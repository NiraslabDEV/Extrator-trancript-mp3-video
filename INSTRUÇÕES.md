# Como Usar o Pop the Balloon Transcript Archiver

## 📋 Requisitos Prévios

- **Windows 10+** (ou Linux/Mac com Python 3.9+)
- **Python 3.9+** instalado ([download](https://www.python.org/downloads/))
  - **IMPORTANTE**: Marque "Add Python to PATH" durante instalação

## 🚀 Setup Inicial (Primeira Vez)

### Opção 1: Usando o .exe (Mais Fácil) ⭐ RECOMENDADO
1. Abra a pasta do projeto
2. Clique 2x em `PopTheBalloon Archiver.exe`
3. Pronto! O app abre em uma janela desktop profissional

**Não precisa instalar nada.**

### Opção 2: Rodar do Código-Fonte (Desenvolvimento)

1. **Abra PowerShell ou CMD** na pasta do projeto
2. **Crie ambiente virtual** (opcional mas recomendado):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. **Instale dependências**:
   ```powershell
   pip install -r requirements.txt
   ```
4. **Rode o app**:
   ```powershell
   python main.py
   ```

O app abre em uma janela desktop nativa (PyQt6) muito mais profissional.

## 🔨 Gerar o Executável Instalável

Se quer criar seu próprio `.exe`:

1. **Instale PyInstaller**:
   ```powershell
   pip install PyInstaller
   ```

2. **Execute o build**:
   ```powershell
   python setup.py
   ```

3. **Pegue em**: `dist/PopTheBalloon Archiver.exe`

Pronto! Agora você tem um executável standalone que roda em qualquer Windows (sem precisar de Python instalado).

## 💾 Como Usar o App

### Interface
O app abre com uma interface desktop profissional com:
- Campo de entrada para URL
- Seletor de pasta
- **Seletor de modo**: Transcrição ou Áudio
- Botão grande de extração
- Tabela com status dos vídeos
- Log detalhado de todas as ações
- Barra de progresso

### Passo 1: Colar URL do Canal
- Procure qualquer vídeo do canal "Pop the Balloon"
- Copie a URL dele (ex: `https://www.youtube.com/watch?v=abc123`)
- **OU** use diretamente o handle do canal: `@popttheballoon`
- Cole no campo "URL do Canal"

### Passo 2: Escolher Pasta de Destino
- Clique botão **"📁 Escolher Pasta"**
- Selecione onde quer salvar as transcrições
- A pasta aparecerá ao lado do botão em verde

### Passo 3: Escolher Modo
- **Para Transcrições**: Clique em "Transcrição" (padrão)
- **Para Áudios**: Clique em "Áudio" (baixa MP3 de máxima qualidade)

### Passo 4: Extrair!
- Clique no botão verde **"EXTRAIR SELECIONADOS"** (texto muda conforme modo)
- O app vai:
  - **Modo Transcrição**: Buscar legendas e salvar como `.txt`
  - **Modo Áudio**: Baixar áudio em MP3 de máxima qualidade
  - Mostra progresso em tempo real

### Passo 4: Acompanhar Progresso
- **Barra de progresso**: % de conclusão
- **Tabela de vídeos**: Status de cada um (✅=ok, ⚠️=aviso, ⏳=processando)
- **Log**: Tudo que o app está fazendo em tempo real

## 📁 Exemplo de Saída

Após rodar, sua pasta contém:

```
Minha_Pasta_Pop_the_Balloon/
├── 2025-04-01 - Episódio 42 - Como crescer relacionamentos.txt
├── 2025-04-02 - Episódio 43 - Dinâmica de grupo.txt
├── 2025-04-03 - Episódio 44 - Lidando com conflitos.txt
└── ... (um arquivo por vídeo)
```

Cada arquivo tem:
```
Título: Episódio 42 - Como crescer relacionamentos
Data: 2025-04-01
================================================================================

Conteúdo da transcrição aqui...
Texto limpo, sem timestamps...
Pronto pra ler ou fazer busca!
```

## 🖥️ Características do App Desktop

- ✅ **Interface profissional** com PyQt6 (nativa do Windows)
- ✅ **Thread independente** - não trava enquanto baixa
- ✅ **Tabela de status** - vê progress de cada vídeo
- ✅ **Log detalhado** - tudo que está acontecendo
- ✅ **Barra de progresso** - % visível
- ✅ **Responsivo** - clica em tudo sem travar
- ✅ **Executável único** - sem dependências
- ✅ **Dark/Light ready** - tema automático do Windows

## ⚠️ Troubleshooting

### "Python não encontrado após instalar"
- Feche e reabra o PowerShell/CMD após instalar Python
- OU reinstale Python marcando "Add Python to PATH"

### "yt-dlp command not found"
- Certifique que executou `pip install -r requirements.txt`
- Se ainda não funcionar: `pip install yt-dlp`

### "Canal não encontrado"
- Verifique URL está correta
- Alguns canais podem estar privados/deletados
- Tente com um vídeo específico em vez de canal

### "Sem legendas para alguns vídeos"
- Normal! Alguns vídeos do canal podem não ter legendas
- O app marca com ⚠️ e continua
- Legendas auto-geradas pelo YouTube geralmente estão disponíveis

### "Permissão negada na pasta"
- Pasta pode estar bloqueada ou em uso
- Escolha outra pasta
- Ou execute o app como Admin

### "Lentidão/Timeout em muitos vídeos"
- Sua internet pode estar lenta
- yt-dlp às vezes toma `timeout`
- Continue deixando rodar, ele tenta novamente
- Canais com 1000+ vídeos podem levar horas

## 🎯 Dicas de Uso

1. **Primeira execução**: Pode parecer lento no início (yt-dlp baixa metadata)
2. **Muitos vídeos**: De noite é melhor (server YouTube menos congestionado)
3. **Organize por tópico**: Crie subpastas para diferentes canais/cursos
4. **Faça backup**: Depois que extrair, copie a pasta para HD externo ou cloud
5. **Monte um índice**: Use o .txt para fazer busca textual depois

## 📦 Distribuição

Se quer distribuir o app para outras pessoas:

1. Gere o `.exe` como descrito acima
2. Crie uma pasta com:
   ```
   PopTheBalloon_Archiver/
   ├── PopTheBalloon Archiver.exe
   ├── README.txt
   └── INSTRUÇÕES.md (este arquivo)
   ```
3. Compacte como ZIP e distribua
4. Pessoas só precisam extrair e clicar no .exe!

## 📞 Support / Issues

Se algo não funcionar:
1. Verifique requisitos (Python 3.9+, internet)
2. Tente rodar em PowerShell como Admin
3. Se erro persiste, veja o **Log** no app (área de texto embaixo)
4. Copie o erro e procure documentação: 
   - [yt-dlp docs](https://github.com/yt-dlp/yt-dlp)
   - [PyQt6 docs](https://www.riverbankcomputing.com/static/Docs/PyQt6/)

---

**Versão**: 2.0 (Desktop PyQt6)
**Última atualização**: Abril 2025  
**Status**: Production Ready  

Aproveite sua coleção de transcrições! 🎉
