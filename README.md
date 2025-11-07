# Jur.IA

Jur.IA é um assistente inteligente integrado ao WhatsApp que utiliza inteligência artificial para processar e resumir documentos jurídicos.

## Visão Geral

O projeto é composto por dois serviços principais:

- **WhatsappService**: Bot do WhatsApp que recebe mensagens e interage com usuários
- **AIDoc**: Serviço de IA que processa documentos usando modelos avançados de linguagem

## Pré-requisitos

- Docker e Docker Compose
- Node.js 18+ (para desenvolvimento local)
- Python 3.11+ (para desenvolvimento local)
- Conta OpenAI com API key válida

## Configuração

### 1. Clonagem do Repositório

```bash
git clone <repository-url>
cd Wrythm
```

### 2. Variáveis de Ambiente

#### WhatsappService (.env)
Crie um arquivo `.env` na pasta `WhatsappService/` com as seguintes variáveis:

```env
AI_RESUMER_BASE_URL=http://localhost:8000
```

#### AIDoc (.env)
Crie um arquivo `.env` na pasta `AIDoc/` com as seguintes variáveis:

```env
OPENAI_API_KEY=sua-chave-api-openai-aqui
```

### 3. Instalação e Execução

#### Usando Docker (Recomendado)

```bash
# Construir e iniciar os serviços
docker-compose up --build
```

#### Desenvolvimento Local

**AIDoc (Python/FastAPI):**
```bash
cd AIDoc
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

A API estará disponível em: http://localhost:8000
Documentação interativa: http://localhost:8000/docs

**WhatsappService (Node.js/TypeScript):**
```bash
cd WhatsappService
npm install
npm run dev
```

## Uso

1. Após iniciar os serviços, o bot do WhatsApp irá gerar um QR code no terminal
2. Escaneie o QR code com seu WhatsApp
3. Envie mensagens para o bot - ele irá processá-las usando a IA integrada

## Funcionalidades

- Processamento inteligente de documentos jurídicos
- Resumos automáticos usando IA avançada
- Integração nativa com WhatsApp
- Suporte a múltiplos provedores de IA (OpenAI, Anthropic)

## Desenvolvimento

### Estrutura do Projeto

```
Wrythm/
├── AIDoc/              # Serviço de IA
│   ├── main.py
│   ├── requirements.txt
│   └── dockerfile
├── WhatsappService/    # Bot WhatsApp
│   ├── src/
│   ├── api/
│   ├── package.json
│   └── dockerfile
└── README.md
```

### Scripts Disponíveis

**WhatsappService:**
- `npm run dev`: Executa em modo desenvolvimento
- `npm run build`: Compila TypeScript

**AIDoc:**
- Execute `python main.py` para iniciar o serviço

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

