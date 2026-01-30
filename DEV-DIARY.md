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

## 29 de Janeiro

Hoje iniciei o projeto e comecei a estruturar o README. Comecei, obviamente, pelo primeiro teste, o 1.1. Após ler, novamente, o teste comecei dividindo o teste em partes, para e ajudar nesse processo decidi criar um projeto no github linkado com o repositório do teste, como o projeto do github tem uma estrutura de kanban achei que seria uma ótima forma de separar as ideia e o que precisa ser feito.

Comecei olhando a API pelo navegador mesmo e entendendo a estrutura de pastas da API e pensando em uma forma de pegar os arquivos evitando erros futuros. Para pegar sempre os últimos 3 trimetre, tive a ideia de pegar o ano atual, acessar pela api e pegar os arquivos, mas cai em outro problema: pela data de postagem dos arquivos percebi que eles não postam no final do ano (o que também é óbvio já que é trimestre kk), então ao acessar no meio do ano tem a grande chance de eles terem postado o arquivo do primeiro trimestre. Dito isso, terei que fazer unma lógica para caso n tenha 3 trimestres, terei que entrar na pasta do ano anterior e pegar os trimestres que faltam.

A principio pensei em fazer uma forma de calcular os trimestres usando essa lógica: `(current_month - 1) // 3 + 1`. Mas não deu muito certo pois a api nem sempre vai postar logo após completar um trimestre, então vou contar a quantidade de arquivos ao requisitar o ano na api, acredito ser a maneira mais segura.

...alguns momentos depois...

Perfeito, agora está funcionando já estou bucando e baixando os arquivos
