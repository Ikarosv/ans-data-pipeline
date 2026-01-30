# Registro de Decisões de Arquitetura - Pipeline ETL

## Contexto

O objetivo deste módulo é extrair dados contábeis da API pública da ANS, processar arquivos de "Despesas com Eventos/Sinistros" dos últimos 3 trimestres e consolidá-los.

## Decisões e Trade-offs

### 1. Estratégia de Processamento: Streaming vs. In-Memory

**Requisito:** Decidir entre processar tudo em memória ou incrementalmente.

**Decisão:** Processamento **Incremental (Stream/Chunks)** com consolidação final.

**Justificativa:**

- **Eficiência de Memória:** Arquivos contábeis governamentais podem variar drasticamente de tamanho. Carregar múltiplos DataFrames na memória RAM simultaneamente aumenta o risco de `MemoryError`, especialmente em ambientes containerizados (Docker/Kubernetes) com recursos limitados.
- **Escalabilidade:** Ao processar arquivo por arquivo e realizar o _append_ em uma lista de buffer, garantimos que o script rode mesmo se o volume de dados triplicar no futuro.

### 2. Tratamento de Inconsistências de Dados

**Requisito:** Lidar com duplicatas, valores zerados e formatos variados.

**Decisões Implementadas:**

- **CNPJs Duplicados:** Optei por **manter a última ocorrência** caso haja duplicidade exata de (CNPJ, Trimestre, Ano), assumindo que o arquivo mais recente ou a linha processada por último é uma retificação. Se a duplicidade for apenas cadastral (mesmo CNPJ, Razão Social diferente), mantemos a Razão Social mais frequente ou a mais recente.
- **Valores Numéricos:** O script converte explicitamente o formato brasileiro (1.000,00) para float (1000.0). Valores não numéricos ou nulos na coluna de despesas são convertidos para `0.0` para evitar quebras em cálculos de agregação (soma), mas são logados como "Warning".
- **Encoding:** Devido à inconsistência nos arquivos governamentais (mistura de `UTF-8`, `Latin-1`, `CP1252`), implementei uma detecção automática com fallback. Tentar abrir apenas como UTF-8 causaria falha em arquivos legados.

### 3. Extração de Arquivos (ZIP)

**Decisão:** Extração em Memória (`io.BytesIO`).

**Justificativa:** Evita I/O de disco desnecessário. Não há necessidade de gravar o `.csv` bruto no disco para depois lê-lo e deletá-lo. O arquivo é baixado, descompactado na RAM, processado e descartado, mantendo o sistema de arquivos limpo.
