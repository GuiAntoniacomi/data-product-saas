# Reddit Pain Signal Scraper

Script para coletar sinais de dor no Reddit. Use na **Semana 2** do projeto para escalar além da pesquisa manual da Semana 1.

---

## Passo 1: Criar app Reddit (5 minutos)

1. Acesse: https://www.reddit.com/prefs/apps
2. Clique em **"create another app..."** (no final da página)
3. Preencha:
   - **name:** `data-pain-scraper` (qualquer nome)
   - **type:** selecione `script`
   - **redirect uri:** `http://localhost:8080` (não importa, não é usado)
4. Clique em **"create app"**
5. Você verá:
   - O **client_id** está logo abaixo do nome do app (string curta)
   - O **client_secret** está no campo "secret"

---

## Passo 2: Configurar credenciais

```bash
# Na pasta scraper/, copie o arquivo de exemplo
cp .env.example .env

# Abra .env e preencha com seus valores reais
# REDDIT_CLIENT_ID=abc123...
# REDDIT_CLIENT_SECRET=xyz456...
# REDDIT_USER_AGENT=data-pain-scraper/1.0 by u/seu_usuario
```

---

## Passo 3: Instalar dependências

```bash
# Na pasta scraper/
pip install -r requirements.txt
```

---

## Passo 4: Rodar o script

```bash
python reddit_scraper.py
```

O script vai:
1. Buscar posts em todos os subreddits configurados (`config.py`)
2. Filtrar por keywords de dor
3. Calcular intensidade de dor (1-5) por engajamento
4. Salvar tudo em `sinais_de_dor_reddit.csv`

---

## Passo 5: Importar para Google Sheets

1. Abra seu Google Sheets de rastreamento
2. Aba **Sinais de Dor** → `Arquivo > Importar`
3. Selecione o CSV gerado
4. Escolha: "Anexar ao final da planilha"
5. Remova duplicatas (linhas que você já inseriu manualmente)

---

## Personalizar buscas

Edite `config.py` para:
- Adicionar/remover subreddits
- Adicionar novas queries de busca
- Ajustar `MIN_SCORE` (padrão: 2) para filtrar mais ou menos ruído
- Mudar `TIME_FILTER` para buscar em períodos diferentes

---

## Troubleshooting

| Erro | Solução |
|------|---------|
| `prawcore.exceptions.ResponseException: received 401` | Verifique client_id e client_secret no `.env` |
| `prawcore.exceptions.NotFound` | Nome do subreddit está errado em `config.py` |
| CSV vazio | Reduza `MIN_SCORE` para 1 ou expanda `TIME_FILTER` para `all` |
| Encoding errado no Excel | Abra como UTF-8 ou importe via Google Sheets |
