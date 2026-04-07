import sys
import subprocess
import json
import os
import re
from html import unescape
from datetime import datetime
from pathlib import Path


def _yt_dlp_cmd():
    """Retorna o caminho do yt-dlp no venv atual ou no PATH do sistema."""
    # Tenta no mesmo venv do Python que está rodando
    base = Path(sys.executable).parent
    candidates = [
        base / "yt-dlp.exe",
        base / "yt-dlp",
        base / "Scripts" / "yt-dlp.exe",
        base / "Scripts" / "yt-dlp",
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    return "yt-dlp"  # fallback: assume no PATH


class TranscriptScraper:
    def __init__(self, output_dir: str, log_callback=None):
        self.output_dir = output_dir
        self.log_callback = log_callback or print
        self.yt = _yt_dlp_cmd()

    def log(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_callback(f"[{timestamp}] {message}")

    def _fetch_flat(self, url: str, timeout: int = 120) -> list:
        """Roda yt-dlp --flat-playlist -J e retorna entries."""
        cmd = [self.yt, "--flat-playlist", "-J", "--no-warnings", url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.returncode != 0:
            self.log(f"Erro yt-dlp: {result.stderr[:300]}")
            return []
        data = json.loads(result.stdout)
        return data.get("entries", [])

    def get_playlist_videos(self, channel_url: str) -> list:
        """Lista vídeos e lives do canal (aba /videos)."""
        try:
            self.log(f"Buscando vídeos: {channel_url}")
            entries = self._fetch_flat(channel_url)

            # Canais podem ter playlist aninhada (uploads)
            if entries and entries[0].get("_type") == "playlist":
                entries = entries[0].get("entries", [])

            videos = []
            for entry in entries:
                if not entry or not entry.get("id"):
                    continue
                live_status = entry.get("live_status", "")
                kind = "live" if live_status in ("is_live", "was_live", "is_upcoming") else "video"
                videos.append({
                    "url": f"https://www.youtube.com/watch?v={entry['id']}",
                    "title": entry.get("title", "Sem título"),
                    "id": entry["id"],
                    "date": entry.get("upload_date"),
                    "kind": kind,
                })

            self.log(f"Encontrados {len(videos)} vídeos/lives")
            return videos

        except subprocess.TimeoutExpired:
            self.log("Timeout ao buscar vídeos. Verifique sua conexão.")
            return []
        except json.JSONDecodeError as e:
            self.log(f"Erro ao processar JSON do yt-dlp: {e}")
            return []
        except Exception as e:
            self.log(f"Erro inesperado: {e}")
            return []

    def get_channel_playlists(self, channel_url: str) -> list:
        """Lista as playlists públicas do canal."""
        try:
            # Normaliza URL base do canal
            base = channel_url.rstrip("/")
            if "/playlists" not in base:
                playlists_url = base + "/playlists"
            else:
                playlists_url = base

            self.log(f"Buscando playlists: {playlists_url}")
            entries = self._fetch_flat(playlists_url, timeout=60)

            playlists = []
            for entry in entries:
                if not entry:
                    continue
                pid = entry.get("id") or entry.get("playlist_id")
                if not pid:
                    continue
                playlists.append({
                    "url": f"https://www.youtube.com/playlist?list={pid}",
                    "title": entry.get("title", "Sem título"),
                    "id": pid,
                    "count": entry.get("playlist_count") or entry.get("n_entries") or "?",
                    "kind": "playlist",
                })

            self.log(f"Encontradas {len(playlists)} playlists")
            return playlists

        except subprocess.TimeoutExpired:
            self.log("Timeout ao buscar playlists.")
            return []
        except Exception as e:
            self.log(f"Erro ao buscar playlists: {e}")
            return []

    def extract_transcript(self, video_url: str, video_title: str) -> str | None:
        """Extrai transcrição de um vídeo (tenta pt, depois pt-BR, depois auto)."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            for lang in ["pt", "pt-BR", "en"]:
                text = self._try_extract(video_url, video_title, lang, tmpdir)
                if text:
                    return text
        return None

    def _try_extract(self, video_url: str, video_title: str, lang: str, tmpdir: str) -> str | None:
        try:
            out_template = os.path.join(tmpdir, "sub.%(ext)s")
            cmd = [
                self.yt,
                "--skip-download",
                "--write-auto-subs",
                "--write-subs",
                "--sub-lang", lang,
                "--convert-subs", "vtt",
                "--no-warnings",
                "-o", out_template,
                video_url,
            ]
            subprocess.run(cmd, capture_output=True, text=True, timeout=90)

            # Procura qualquer .vtt gerado
            for fname in os.listdir(tmpdir):
                if fname.endswith(".vtt"):
                    fpath = os.path.join(tmpdir, fname)
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    text = self._parse_vtt(content)
                    if text.strip():
                        self.log(f"Legenda encontrada ({lang}): {video_title[:50]}")
                        return text
            return None

        except subprocess.TimeoutExpired:
            self.log(f"Timeout ao extrair: {video_title[:50]}")
            return None
        except Exception as e:
            self.log(f"Erro ao extrair {video_title[:50]}: {e}")
            return None

    def _parse_vtt(self, content: str) -> str:
        """Extrai texto limpo de um VTT, sem duplicatas e com parágrafos."""
        # Cada bloco VTT é separado por linha em branco
        blocks = re.split(r"\n\n+", content)
        seen = []
        for block in blocks:
            lines = block.splitlines()
            text_parts = []
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
                    continue
                if "-->" in line:
                    continue
                if re.match(r"^\d+$", line):  # número de sequência SRT/VTT
                    continue
                # Remove tags como <00:00:00.000> e <c>
                line = re.sub(r"<[^>]+>", "", line).strip()
                # Decodifica entidades HTML (&gt; → >, &amp; → &, etc.)
                line = unescape(line)
                if line:
                    text_parts.append(line)

            if not text_parts:
                continue

            sentence = " ".join(text_parts)

            # Evita duplicatas exatas de blocos consecutivos (legendas sobrepostas)
            if seen and seen[-1] == sentence:
                continue
            # Evita blocos que são apenas sufixo do anterior (sobreposição parcial)
            if seen and seen[-1].endswith(sentence):
                continue

            seen.append(sentence)

        return "\n".join(seen)

    def save_transcript(self, video_title: str, transcript: str, upload_date: str | None = None) -> bool:
        """Salva transcrição em arquivo .txt."""
        try:
            if upload_date and len(upload_date) == 8:
                # YYYYMMDD -> YYYY-MM-DD
                date_str = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
            else:
                date_str = datetime.now().strftime("%Y-%m-%d")

            filename = f"{date_str} - {video_title}.txt"
            filename = self._sanitize_filename(filename)
            filepath = os.path.join(self.output_dir, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"Título: {video_title}\n")
                f.write(f"Data: {date_str}\n")
                f.write("=" * 80 + "\n\n")
                f.write(transcript)

            self.log(f"Salvo: {filename}")
            return True
        except Exception as e:
            self.log(f"Erro ao salvar: {e}")
            return False

    def download_audio(self, video_url: str, video_title: str, upload_date: str | None = None) -> bool:
        """Baixa melhor áudio disponível (mp3 se ffmpeg presente, webm/m4a caso contrário)."""
        try:
            if upload_date and len(upload_date) == 8:
                date_str = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
            else:
                date_str = datetime.now().strftime("%Y-%m-%d")

            filename = f"{date_str} - {video_title}.%(ext)s"
            filename = self._sanitize_filename(filename)
            out_template = os.path.join(self.output_dir, filename)

            self.log(f"Baixando áudio: {video_title[:50]}...")

            ffmpeg = self._ffmpeg_path()
            if ffmpeg:
                cmd = [
                    self.yt,
                    "--extract-audio",
                    "--audio-format", "mp3",
                    "--audio-quality", "0",
                    "--ffmpeg-location", ffmpeg,
                    "--no-warnings",
                    "-o", out_template,
                    video_url,
                ]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    path = out_template.replace("%(ext)s", "mp3")
                    if os.path.exists(path):
                        self.log(f"Salvo: {os.path.basename(path)}")
                        return True
                self.log(f"Erro ffmpeg: {result.stderr[:200]}")

            self.log("ffmpeg nao encontrado — baixando no formato nativo...")
            cmd = [self.yt, "-f", "bestaudio", "--no-warnings", "-o", out_template, video_url]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                for ext in ["webm", "m4a", "opus", "ogg"]:
                    path = out_template.replace("%(ext)s", ext)
                    if os.path.exists(path):
                        self.log(f"Salvo: {os.path.basename(path)}")
                        return True

            self.log(f"Erro ao baixar audio: {result.stderr[:300]}")
            return False

        except subprocess.TimeoutExpired:
            self.log(f"Timeout ao baixar áudio: {video_title[:50]}")
            return False
        except Exception as e:
            self.log(f"Erro ao baixar áudio {video_title[:50]}: {e}")
            return False

    def _ffmpeg_path(self) -> str | None:
        """Retorna caminho do ffmpeg (sistema ou static-ffmpeg)."""
        # Tenta ffmpeg do sistema
        try:
            r = subprocess.run(["ffmpeg", "-version"], capture_output=True, timeout=5)
            if r.returncode == 0:
                return "ffmpeg"
        except Exception:
            pass
        # Tenta static-ffmpeg (instalado via pip)
        try:
            import static_ffmpeg
            static_ffmpeg.add_paths()
            import shutil
            path = shutil.which("ffmpeg")
            if path:
                return path
        except Exception:
            pass
        return None

    def _sanitize_filename(self, filename: str) -> str:
        invalid = '<>:"/\\|?*'
        for c in invalid:
            filename = filename.replace(c, "_")
        return filename[:200]  # limita tamanho
