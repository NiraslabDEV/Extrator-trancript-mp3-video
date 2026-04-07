# SPEC.md - Especificação Técnica Detalhada

## 1. Stack Tecnológico
- **Linguagem**: Python 3.9+
- **UI Desktop**: Flet (conversível para web, móvel, desktop)
- **Scraper**: yt-dlp (fork mantido do youtube-dl)
- **Persistência**: Arquivos .txt + SQLite (banda peso para histórico)
- **Packaging**: flet pack (gera executável Windows)

## 2. Arquitetura do Projeto

```
PopTheBalloon_Transcript_Archiver/
├── main.py                 # Entry point (app Flet)
├── requirements.txt        # Dependências Python
├── core/
│   ├── __init__.py
│   └── scraper.py         # Classe TranscriptScraper
├── ui/
│   ├── __init__.py
│   └── components.py      # Componentes reutilizáveis (futuro)
├── SPEC.md                # Este arquivo
└── INSTRUÇÕES.md          # Como usar
```

## 3. Componentes de UI

### 3.1 Tela Principal
- **Título**: "Pop the Balloon - Transcrição Archiver" (tamanho 28, azul)
- **Campo URL**: TextField grande com hint text
- **Botão Pasta**: Abre file picker para selecionar destino
- **Status Pasta**: Mostra caminho atual
- **Botão Principal**: "EXTRAIR TODAS AS TRANSCRIÇÕES" (verde, grande, 60px altura)
- **Progress Bar**: Mostra % do processamento
- **Lista de Vídeos**: ListView com status em tempo real (✅ ⚠️ ⏳ ❌)
- **Log Area**: TextArea read-only mostrando cada ação
- **Footer**: Informação sobre versão (v1.0)

## 4. Fluxo de Execução

```
1. Usuário cola URL do canal
2. Clica em "Escolher Pasta"
3. Seleciona pasta de destino
4. Clica em "EXTRAIR TODAS"
   ├─ Valida URL
   ├─ Executa: yt-dlp --flat-playlist --dump-json <URL>
   │  └─ Parse JSON → lista de vídeos
   ├─ Para cada vídeo em paralelo (ou sequencial):
   │  ├─ Download das legendas: yt-dlp --skip-download --write-auto-subs
   │  ├─ Parse SRT/VTT → texto limpo
   │  ├─ Salva <YYYY-MM-DD - Título>.txt
   │  └─ Atualiza UI (✅/⚠️/❌)
   └─ Exibe mensagem de sucesso
```

## 5. Detalhes de Implementação

### 5.1 Extração de Legendas
```bash
yt-dlp \
  --skip-download \                   # Não baixa vídeo
  --write-auto-subs \                 # Extrai auto-subs se não houver manualmente
  --sub-lang pt \                     # Prioriza português
  -o "%(title)s.%(ext)s" \           # Nome do arquivo
  <VIDEO_URL>
```

### 5.2 Limpeza de Transcrição
- Remove timestamps (HH:MM:SS --> HH:MM:SS)
- Preserva o texto original (sem IA)
- Estrutura: 
  ```
  Título: [Título do vídeo]
  Data: [YYYY-MM-DD]
  ========================================
  [Texto da transcrição limpo]
  ```

### 5.3 Naming Convention
- Formato: `YYYY-MM-DD - Título Completo do Vídeo.txt`
- Sanitização: Remove caracteres inválidos (< > : " / \ | ? *)
- Exemplo: `2025-04-07 - Episódio 42 - Como crescer relacionamento.txt`

## 6. Tratamento de Erros

| Erro | Tratamento |
|------|-----------|
| URL inválida | Validar regex, mostrar snackbar |
| Canal não existe | Log "Canal não found", parar |
| Sem legendas | Marcar com ⚠️, continuar próximo |
| Sem permissão pasta | Mostrar erro, sugerir outra pasta |
| Timeout yt-dlp | Retry 1x, depois marcar ❌ |
| Sem internet | Detectar no início, mostrar erro |

## 7. Performance

- **Latência esperada**: 
  - 10 vídeos: ~2-3 min
  - 100 vídeos: ~20-30 min (depende de velocidade internet)
- **Memória**: <500 MB para 1000+ vídeos
- **Storage**: ~1-2 MB por vídeo (texto apenas)

## 8. Escalabilidade (Fase 2)

- [ ] Busca full-text em todas transcrições
- [ ] Exportar para single .pdf
- [ ] Filter por data/título na UI
- [ ] Database SQLite para histórico + dedup
- [ ] Modo batch (processar múltiplos canais)
- [ ] Análise com LLM local (ollama)

## 9. Validação de Entrada

```python
# URL válida: uma destas
- https://www.youtube.com/channel/UCCCC123
- https://www.youtube.com/@NomeCanal
- https://www.youtube.com/c/NomeCanal
- @NomeCanal (auto-completar para URL)
```

## 10. Saída Esperada

Após sucesso, a pasta contém:
```
Transcrições_Pop_the_Balloon/
├── 2025-04-01 - Episódio 1 - Primeiro Video.txt
├── 2025-04-02 - Episódio 2 - Segundo Video.txt
├── 2025-04-03 - Episódio 3 - Terceiro Video.txt
└── ...
```

Cada .txt tem estrutura similar:
```
Título: Episódio 1 - Primeiro Video
Data: 2025-04-01
================================================================================

Conteúdo da transcrição aqui sem timestamps...
Próxima frase aqui...
E por aí vai...
```

## 11. Requisitos Não-Funcionais

- ✅ Funciona offline após yt-dlp instalado
- ✅ Sem autenticação necessária
- ✅ Sem API key do YouTube
- ✅ Executa localmente 100%
- ✅ UI responsiva durante download
- ✅ Suporta cancelamento mid-process

## 12. Configuração de Deployment

Para gerar .exe:
```bash
pip install -r requirements.txt
flet pack main.py \
  --name "PopTheBalloon Archiver" \
  --icon icon.png \
  --hidden-import=core \
  --hidden-import=urllib3
```

Resultado: `dist/PopTheBalloon Archiver.exe`
