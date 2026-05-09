# Data Product SaaS

Repositório de trabalho para construir um negócio de consultoria em Data Engineering com evolução para produto SaaS — partindo de validação de nicho até o primeiro contrato pago.

## O que é isso

Um projeto paralelo de 12 semanas para transformar expertise em BigQuery, Looker e pipelines de dados em receita recorrente, sem abandonar o emprego atual.

**Modelo de evolução:**
```
Consultoria one-off ($3k–6k)  →  Retainer mensal ($1–2k/mês)  →  SaaS ($200–500/mês)
```

**Nichos alvo:** E-commerce (Shopify + Ads), SaaS startups, Redes de franquias

## Estrutura do repositório

```
├── planejamento-data-product.md   # Roadmap completo das 12 semanas
├── scraper/
│   ├── reddit_scraper.py          # Coleta sinais de dor no Reddit (PRAW)
│   ├── config.py                  # Subreddits, queries e configurações
│   ├── .env.example               # Template de credenciais (não subir o .env real)
│   ├── requirements.txt           # Dependências Python
│   └── README_scraper.md          # Guia de setup e uso
└── templates/
    └── planilha_sinais_dor.csv    # Template para Google Sheets (4 abas)
```

## Quick start — scraper de validação

```bash
# 1. Instalar dependências
pip install -r scraper/requirements.txt

# 2. Configurar credenciais Reddit
cp scraper/.env.example scraper/.env
# editar scraper/.env com suas credenciais
# (veja scraper/README_scraper.md para criar o app Reddit)

# 3. Rodar
python scraper/reddit_scraper.py
# gera: sinais_de_dor_reddit.csv
```

## Roadmap resumido

| Semana | Fase | Objetivo |
|--------|------|----------|
| 0 | Preparação | Case study, LinkedIn, ferramentas |
| 1–2 | Descoberta | 50+ sinais de dor coletados |
| 3–4 | Validação | 5–7 calls, Problem Brief escrito |
| 5–6 | Prototipagem | MVP funcional em ≤14 dias |
| 7–8 | Primeira venda | 1 contrato fechado, ≥R$10k |
| 9–12 | Iteração | NPS ≥8, 1 referral ou recontrato |

Detalhes completos no [`planejamento-data-product.md`](./planejamento-data-product.md).
