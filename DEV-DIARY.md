## 28 de Janeiro

Dia em que recebi o teste. Após receber tirei o dia para entender o teste e entender os desafios que teria para resolver. Comecei escolhendo a estrutura de pasta que melhor atenderia ás necessidades do projeto. E achei melhor seguir com uma abordagem [monorepo](https://medium.com/@julakadaredrishi/monorepos-a-comprehensive-guide-with-examples-63202cfab711). E imaginei mais ou menos assim:

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

Mas acredito que possa ocorrer alterações no meio do caminho.
