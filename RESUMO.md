# Resumo do Projeto - PopTheBalloon Transcript Archiver

## Estrutura do Projeto
```
trascript/
├── main.py              # App principal com UI Flet
├── core/
│   ├── __init__.py
│   └── scraper.py       # Lógica de extração de transcrições e áudio
├── requirements.txt     # Dependências
├── run.bat             # Clique duplo para rodar
├── test_audio.py       # Teste de download de áudio
├── CLAUDE.md           # Especificações originais do projeto
└── RESUMO.md           # Este arquivo
```

---

## Funcionalidades Implementadas

### Interface (main.py)
- Campo para URL do canal do YouTube
- Botão para escolher pasta de destino
- Seletor de modo: **Transcrição** ou **Áudio**
- Busca de vídeos do canal (carrega lista completa)
- Checkboxes para seleção individual de vídeos
- Filtros de tipo: **Todos / Vídeos / Lives / Playlists**
- Campo de busca por título (filtra em tempo real)
- Botão "Sel. Visíveis" — seleciona apenas os filtrados na tela
- Botão "Extrair/Baixar Selecionados"
- Botão "Parar" para interromper o processo
- Barra de progresso em tempo real
- Área de logs

### Scraper (core/scraper.py)
- `get_playlist_videos()` — lista vídeos e lives do canal
- `get_channel_playlists()` — lista playlists públicas do canal
- `extract_transcript()` — extrai transcrição (tenta PT, PT-BR, EN)
- `_parse_vtt()` — converte VTT para texto limpo sem timestamps
- `save_transcript()` — salva .txt com data real de publicação
- `download_audio()` — baixa em MP3 (com ffmpeg) ou webm/m4a (sem ffmpeg)
- `_ffmpeg_path()` — detecta ffmpeg do sistema ou do pacote static-ffmpeg

### Dependências
- `flet>=0.24.0` — UI desktop
- `yt-dlp>=2024.11.0` — extração de vídeos/legendas/áudio
- `static-ffmpeg>=2.5` — ffmpeg embutido via pip (sem instalar no sistema)

---

## Bugs Corrigidos (Claude — após Grok quebrar)

### 1. App travava/fechava ao mostrar lista de vídeos
**Causa:** O Grok adicionou `append_log()` dentro do loop de render para cada vídeo.
Com 230 vídeos isso gerava ~460 chamadas de `page.update()` de uma vez, travando o Flet.
**Correção:** Removidos todos os logs de debug do `render_list()`. Agora há apenas
um único `page.update()` ao final do render.

### 2. "Selecionar Todos" selecionava todos os 230 mesmo com filtro ativo
**Causa:** `toggle_all` usava `selected.get(i, True)` como default, o que tratava
vídeos sem entrada no dict como já selecionados, causando comportamento errado.
**Correção:** Mudado para `selected.get(i, False)`. O botão agora age apenas
nos índices visíveis pelo filtro/busca atual.

### 3. `set_mode()` chamado antes de `btn_extract` existir → crash na abertura
**Causa:** O Grok chamava `set_mode("transcript")` no final do arquivo, após `page.add()`,
mas depois foi movido para antes dos botões serem criados, causando `NameError: btn_extract`.
**Correção:** `set_mode()` e `set_kind()` agora são chamados após todos os botões
serem criados, mas antes de `page.add()`.

### 4. Download de áudio falhava sem ffmpeg
**Causa:** `download_audio()` usava `--extract-audio --audio-format mp3` que exige
ffmpeg instalado no sistema. Sem ele, o yt-dlp retornava erro de post-processing.
**Correção:** Adicionado `static-ffmpeg` (pip install) que fornece o binário do ffmpeg
embutido. O scraper detecta automaticamente via `_ffmpeg_path()` e passa
`--ffmpeg-location` ao yt-dlp. Fallback para formato nativo (webm) se nada funcionar.

---

## Próximas Tasks (backlog)

### ALTA PRIORIDADE

#### 1. Mostrar % de progresso do download de cada arquivo
- Atualmente a barra só avança entre vídeos (1/10, 2/10...)
- Quero ver o progresso interno de cada download (ex: "Baixando... 47%")
- **Como fazer:** yt-dlp tem `--progress` e suporte a hooks de progresso via Python API
  em vez de subprocess. Alternativa: parsear o stdout do yt-dlp em tempo real.

#### 2. Aceitar link de vídeo individual (não só canal)
- Colar `https://www.youtube.com/watch?v=XXXX` e baixar só aquele vídeo
- **Como fazer:** Detectar se a URL contém `watch?v=` ou `/shorts/` → tratar como
  vídeo único, pular a etapa de listar canal, ir direto para extração/download.

#### 3. Download do vídeo completo (MP4)
- Baixar o vídeo em si (não só áudio)
- **Quando usar:** Por enquanto não é prioridade, mas a infraestrutura já está pronta.
- **Como fazer:** Adicionar modo "Vídeo" no seletor de modo. Usar yt-dlp com
  `-f bestvideo+bestaudio --merge-output-format mp4 --ffmpeg-location <path>`.
  Requer ffmpeg (já temos via static-ffmpeg).

### MÉDIA PRIORIDADE

#### 4. Evitar baixar duplicatas
- Se já existe um arquivo com aquele nome na pasta, pular.
- **Como fazer:** Verificar se o arquivo `.txt` ou `.mp3` já existe antes de processar.

#### 5. Exportar todas as transcrições em um único arquivo
- Útil para análise com LLM — um `.txt` gigante com todos os episódios.

---

## Formato dos Arquivos de Saída

**Transcrições:**
```
2025-04-01 - Ep 92_ Pop The Balloon Or Find Love.txt
```
Conteúdo:
```
Título: Ep 92: Pop The Balloon Or Find Love
Data: 2025-04-01
================================================================================

>> Hello everyone and welcome back...
>> My name is Russ.
```

**Áudios:**
```
2025-04-01 - Ep 92_ Pop The Balloon Or Find Love.mp3
```
