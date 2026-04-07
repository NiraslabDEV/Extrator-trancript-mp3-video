# Pop the Balloon - Transcript & Audio Archiver

Um aplicativo desktop para baixar transcrições e áudios de canais do YouTube, focado no canal "Pop the Balloon" para arquivar relacionamentos interpessoais.

![Interface do App](https://via.placeholder.com/800x400/4CAF50/FFFFFF?text=Pop+the+Balloon+Archiver)

## ✨ Funcionalidades

### 🎯 Extração de Transcrições
- Baixe legendas automaticamente de vídeos do YouTube
- Suporte a português, português brasileiro e inglês
- Texto limpo sem timestamps ou tags
- Arquivos organizados por data e título

### 🎵 Download de Áudio
- Baixe áudios em MP3 de máxima qualidade
- Funciona mesmo sem ffmpeg instalado (formatos nativos)
- Organização automática por data

### 🖥️ Interface Desktop Moderna
- Interface intuitiva com Flet
- Seletor de modo: Transcrição ou Áudio
- Busca e filtros avançados
- Barra de progresso em tempo real
- Logs detalhados de todas as operações

## 🚀 Instalação

### Pré-requisitos
- **Windows 10+**
- **Python 3.9+** ([download](https://www.python.org/downloads/))
- **ffmpeg** (opcional, mas recomendado para MP3)

### Instalação Automática (Recomendado)

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/NiraslabDEV/Extrator-trancript-mp3-video.git
   cd Extrator-trancript-mp3-video
   ```

2. **Instale dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o app:**
   ```bash
   python main.py
   ```

### Instalação Manual

1. **Instale Python 3.9+**
2. **Clone ou baixe os arquivos**
3. **Instale dependências:**
   ```bash
   pip install flet yt-dlp
   ```
4. **(Opcional) Instale ffmpeg:**
   ```bash
   # Windows (via winget)
   winget install ffmpeg

   # Ou baixe em: https://ffmpeg.org/download.html
   ```

## 💡 Como Usar

### 1. Buscar Vídeos
- Cole a URL do canal (ex: `https://www.youtube.com/@poptheballoon`)
- Clique em **"Buscar Vídeos"**
- O app lista todos os vídeos encontrados

### 2. Escolher Modo
- **Transcrição**: Para baixar legendas como texto
- **Áudio**: Para baixar áudios em MP3

### 3. Selecionar e Baixar
- Marque os vídeos desejados
- Escolha a pasta de destino
- Clique em **"Extrair Selecionados"** ou **"Baixar Áudios"**

### 4. Acompanhar Progresso
- Barra de progresso mostra o andamento
- Logs em tempo real informam cada etapa
- Arquivos são salvos automaticamente

## 📁 Estrutura de Saída

### Transcrições
```
PopTheBalloon_Transcripts/
├── 2026-04-01 - Episódio 91 - Pop The Balloon Or Find Love.txt
├── 2026-04-02 - Episódio 92 - Pop The Balloon Or Find Love.txt
└── ...
```

### Áudios
```
PopTheBalloon_Audios/
├── 2026-04-01 - Episódio 91 - Pop The Balloon Or Find Love.mp3
├── 2026-04-02 - Episódio 92 - Pop The Balloon Or Find Love.mp3
└── ...
```

## 🛠️ Arquitetura do Projeto

```
Extrator-trancript-mp3-video/
├── main.py                 # Interface principal (Flet)
├── core/
│   ├── __init__.py
│   └── scraper.py          # Lógica de extração yt-dlp
├── ui/
│   └── __init__.py         # Módulos UI (expansível)
├── requirements.txt        # Dependências Python
├── run.bat                # Script de execução Windows
├── CLAUDE.md              # Documentação técnica
├── SPEC.md                # Especificações detalhadas
├── INSTRUÇÕES.md          # Guia completo de uso
└── README.md              # Este arquivo
```

## 🔧 Tecnologias Utilizadas

- **Flet**: Framework para interfaces desktop modernas
- **yt-dlp**: Biblioteca para download de vídeos/áudios YouTube
- **ffmpeg**: Conversão de áudio (opcional)
- **Python 3.9+**: Linguagem principal

## 📋 Funcionalidades Avançadas

### Filtros e Busca
- **Todos/Vídeos/Lives/Playlists**: Filtre por tipo de conteúdo
- **Busca por título**: Encontre vídeos específicos rapidamente
- **Seleção múltipla**: Marque/desenarque todos os visíveis

### Tratamento de Erros
- **Verificação de dependências**: Detecta problemas antes de iniciar
- **Fallback de formatos**: Funciona mesmo sem ffmpeg
- **Timeouts inteligentes**: Evita travamentos
- **Logs detalhados**: Debug completo de operações

## 🎯 Casos de Uso

### Arquivo de Relacionamentos
- **Canal Pop the Balloon**: Preserve discussões sobre relacionamentos
- **Conteúdo educativo**: Arquive aulas e palestras
- **Podcasts**: Converta episódios para texto/áudio

### Pesquisa e Análise
- **Busca textual**: Encontre tópicos específicos
- **Análise de conteúdo**: Estude padrões de conversa
- **Backup offline**: Mantenha conteúdo disponível

## 🐛 Troubleshooting

### "ffmpeg não encontrado"
- Instale ffmpeg ou use modo áudio (funciona com formatos nativos)
- Download: https://ffmpeg.org/download.html

### "Canal não encontrado"
- Verifique se a URL está correta
- Alguns canais podem ser privados

### "Sem legendas"
- Vídeos podem não ter legendas disponíveis
- O app pula automaticamente

### App não abre
- Execute `pip install -r requirements.txt`
- Verifique se Python está no PATH

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

## 🙏 Agradecimentos

- **YouTube** e **Pop the Balloon** pelo conteúdo incrível
- **yt-dlp** pela incrível biblioteca de extração
- **Flet** pelo framework de UI desktop

---

**Desenvolvido com ❤️ para preservar conhecimento e relacionamentos**

⭐ **Dê uma estrela se este projeto te ajudou!**</content>
<parameter name="filePath">C:\Users\Gabriel\Desktop\trascript\README.md