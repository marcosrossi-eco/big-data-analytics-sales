
@'
# Big Data Analytics — Sales Pipeline

## Visão geral

Projeto de análise de dados de vendas desenvolvido em Python com pandas e matplotlib. O pipeline processa dados de varejo, realiza limpeza e transformação e gera indicadores e gráficos para apoiar a análise comercial.

## Objetivos

- Construir um pipeline de dados reproduzível.
- Limpar e transformar dados de vendas.
- Identificar países com maior faturamento.
- Analisar os produtos com maior quantidade vendida.
- Acompanhar a evolução mensal do faturamento.
- Gerar relatórios CSV e gráficos PNG.

## Tecnologias

- Python
- pandas
- matplotlib
- openpyxl
- pytest

## Estrutura

```text
big-data-analytics-sales/
├── data/
│   ├── raw/
│   └── processed/
├── reports/
├── src/
│   ├── ingest.py
│   ├── transform.py
│   └── analytics.py
├── spark/
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

## Como executar

Crie e ative um ambiente virtual e instale as dependências:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Coloque o arquivo `Online Retail.xlsx` em `data/raw/` e execute:

```powershell
python src/ingest.py
python src/transform.py
python src/analytics.py
```

## Relatórios gerados

- `reports/sales_by_country.csv` — faturamento por país.
- `reports/top_products.csv` — quantidade vendida por produto.
- `reports/sales_by_month.csv` — faturamento mensal.
- Arquivos PNG correspondentes — visualizações dos indicadores.

## Resultados observados

Na execução atual, o Reino Unido liderou o faturamento, com aproximadamente 9,03 milhões em unidades monetárias do conjunto de dados. O produto `PAPER CRAFT , LITTLE BIRDIE` liderou a quantidade vendida, com 80.995 unidades.

Os valores representam faturamento calculado sobre os registros mantidos após a limpeza, não lucro líquido. A moeda não foi confirmada neste relatório.

## Fonte dos dados

UCI Machine Learning Repository — Online Retail:
https://archive.ics.uci.edu/dataset/352/online+retail

## Próximas evoluções

- Testes automatizados do pipeline.
- Processamento distribuído com PySpark.
- Integração contínua com GitHub Actions.
'@ | Set-Content -Encoding utf8 README.md
