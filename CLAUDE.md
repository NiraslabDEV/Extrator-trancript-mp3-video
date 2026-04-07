# CLAUDE.md - PopTheBalloon Transcript Archiver

## Constitution (Regras obrigatórias para você seguir)
- Proibição total de vibe coding: só gere código depois de entender toda a spec.
- Use Python + Flet para criar um app desktop bonito e simples.
- Use yt-dlp para extrair transcrições (melhor ferramenta atual).
- Tudo deve rodar localmente, sem autenticação.
- Crie um único executável fácil de rodar (use flet pack no final).
- UI deve ser intuitiva: campo grande para URL + botão grande + progresso + log.
- Salve cada transcrição como arquivo .txt limpo em uma pasta escolhida pelo usuário.
- Use SQLite opcional para registrar o que já foi baixado (evitar duplicatas).

## PRD - O que o usuário quer
- App desktop simples.
- Cola link do canal → clica em Extrair Tudo.
- Cria pasta com um .txt por vídeo (nome: "AAAA-MM-DD - Título do Vídeo.txt").
- Mostra progresso em tempo real.
- Funciona offline após instalação.
- Foco no canal "Pop the Balloon" para montar acervo de relações interpessoais.

## Spec Técnica
- Bibliotecas principais: flet, yt-dlp, sqlite3 (opcional)
- Tela principal:
  - TextField grande para URL do canal
  - ElevatedButton "Escolher Pasta de Destino"
  - ElevatedButton grande "Extrair Todas as Transcrições"
  - ProgressBar + ListView com status dos vídeos
  - Textarea para logs
- Fluxo:
  1. Validar URL
  2. Usar yt-dlp para listar todos os vídeos do canal (--flat-playlist)
  3. Para cada vídeo: yt-dlp --skip-download --write-auto-subs --write-subs --sub-lang pt --convert-subs srt ou vtt
  4. Limpar o texto (remover timestamps se possível, ou manter simples)
  5. Salvar como .txt
- Tratamento de erros: canal sem legendas, rate limit, sem internet, pasta sem permissão.

## Tarefas para você (Claude Code) gerar agora
Crie a estrutura completa do projeto com:
- main.py (app Flet completo)
- requirements.txt
- Pasta core/ com scraper.py (funções de extração)
- Pasta ui/ com telas
- Instruções claras de como rodar e gerar o .exe com `flet pack`

Mantenha simples, bonito e robusto. Priorize usabilidade.
2. SPEC.md (especificação mais detalhada — cole também)
Markdown# SPEC.md - Detalhes Técnicos

## Stack
- Linguagem: Python 3.11+
- UI: Flet (mais simples possível)
- Scraper: yt-dlp
- Armazenamento: arquivos .txt + SQLite leve para histórico

## Comportamento esperado
- Usuário cola URL do canal (suporte a @handle, /channel/ID ou /c/name)
- App pergunta ou lembra última pasta usada
- Botão principal inicia o processo
- Durante execução: mostra quantos vídeos encontrados, progresso atual, nome do vídeo sendo processado
- Cada .txt deve conter o título do vídeo no topo + texto completo da transcrição limpa

## Ideias de melhoria (fase 2, se quiser depois)
- Remover timestamps automaticamente
- Busca dentro de todas as transcrições
- Exportar para um único arquivo grande
- Análise automática com LLM local (opcional)

Gere o código completo seguindo esta spec.
3. INSTRUÇÕES.md (como usar depois que o Claude gerar)
Markdown# Como usar este projeto

1. Instale Python (se ainda não tiver)
2. Crie uma pasta nova e coloque todos os arquivos gerados
3. Rode no terminal: pip install -r requirements.txt
4. Rode o app: python main.py
5. Para gerar o .exe (Windows): flet pack main.py --name "PopBalloon Archiver"

Depois de ter o .exe, é só clicar duas vezes e usar.

Pasta de saída exemplo:
PopTheBalloon_Transcripts/
   2025-04-01 - Episódio X - Título Completo.txt
   ...