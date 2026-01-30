# TESTE INTUITIVE CARE

## Sumário

- [Estrutura de Pastas](#estrutura-de-pastas)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Integração com a API](#integração-com-a-api)
  - [1.1 Acesso e Download dos dados da API](#11-acesso-e-download-dos-dados-da-api)

## Estrutura de pastas

```pl
intuitive_care_teste/
├── data/                  # Arquivos brutos e processados
│   └── raw/               # Pasta onde ficará os arquivos .zip
├── docs/                  # Documentação extra e diagramas
├── etl/                   # Extração, Transformação e Carregamento
│   ├── __init__.py
│   ├── downloader.py      # Baixar arquivos FTP
│   ├── processor.py       # Limpeza e normalização com Pandas
│   └── validator.py       # Regras de validação (Pydantic ou Pandera)
├── backend/
│   ├── app/
│   │   ├── models.py      # Modelos do Banco (SQLAlchemy)
│   │   ├── routers.py     # Endpoints da API
│   │   └── main.py        # Entrypoint FastAPI
├── frontend/
├── sql/                   # Scripts .sql puros solicitados
├── docker-compose.yml     # Docker para subir banco e api
├── README.md
└── requirements.txt
```

## Configuração do Ambiente

Este projeto utiliza Python 3.x. Para garantir a integridade das dependências, siga os passos abaixo:

1. **Crie o ambiente virtual:**
   ```bash
   python -m venv .venv
   ```
2. **Ative o ambiente:**
   - **Windows:**
     ```bash
     .\.venv\Scripts\activate
     ```
   - **Linux/MacOS**
     ```bash
     source .venv/bin/activate
     ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

## Integração com a API

### 1.1 Acesso e Download dos dados da API

Para a extração dos dados, foi desenvolvida uma solução de **Web Scraping** robusta utilizando a biblioteca `BeautifulSoup`. A abordagem foge de URLs estáticas (hardcoded) em favor de uma descoberta dinâmica, garantindo que o script continue funcionando mesmo que a ANS atualize os trimestres ou altere a nomenclatura dos arquivos.

**Decisões Técnicas e Trade-offs:**

- **Estratégia de Busca (Heurística Temporal):**
  - O script inicia a busca pelo ano corrente. Caso não encontre os 3 trimestres solicitados (ex: estamos no início do ano), ele recua automaticamente para o ano anterior.
  - _Justificativa:_ Isso evita requisições desnecessárias a anos antigos e garante que sempre teremos os dados mais recentes disponíveis, atendendo ao requisito de resiliência.

- **Gerenciamento de Memória (Streaming):**
  - O download é realizado utilizando `stream=True` da biblioteca `requests`, gravando o arquivo no disco em _chunks_ (pedaços) de 8KB.
  - _Justificativa:_ Arquivos de demonstrações contábeis podem ser extensos. Carregar o arquivo inteiro na memória RAM antes de salvar causaria gargalos ou erros de _Out of Memory_ em ambientes com recursos limitados (containers/fargate). O streaming mantém o consumo de RAM baixo e constante.

- **Idempotência:**
  - Antes de iniciar o download, o script verifica se o arquivo já existe no diretório de destino.
  - _Justificativa:_ Evita consumo de banda desnecessário e acelera a re-execução do pipeline em caso de falhas parciais ou testes repetidos.

- **Organização dos Dados (Raw Layer):**
  - Os arquivos são salvos estruturalmente em `data/raw/{ano}/{trimestre}/`, preservando a rastreabilidade da origem.

**Bibliotecas utilizadas:**

- `requests`: Para conexões HTTP persistentes (`Session`) e performáticas.
- `beautifulsoup4`: Para navegar na árvore HTML do diretório da ANS.
- `logging`: Para observabilidade do processo em tempo real.
