# TESTE INTUITIVE CARE

## Sumário

- [Estrutura de Pastas](#estrutura-de-pastas)
- [Configuração do Ambiente](#configuração-do-ambiente)

## Estrutura de pastas

```pl
intuitive_care_teste/
├── data/                  # Arquivos brutos e processados (ignorados no git)
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
