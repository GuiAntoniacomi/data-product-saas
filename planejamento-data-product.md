# Planejamento: Data Product SaaS
> Versão 2.0 — Maio 2026  
> Autor: Guilherme  
> Objetivo: Construir autonomia financeira com expertise em Data Engineering, sem abandonar emprego atual

---

## Visão & Princípios

### A Tese Central
> *"Você não está aprendendo a vender. Você está resolvendo um problema com métrica clara para alguém que já sofre com ele. Isso se vende sozinho."*

### Os 3 Pilares
1. **Validação antes de construção** — nunca desenvolver algo que ninguém pediu
2. **Consultoria → Produto** — aprender com clientes reais antes de automatizar
3. **5-10h/semana** — não é uma startup, é um projeto paralelo com risco controlado

### O que você TEM (e muitos não têm)
- [ ] Expertise em BigQuery, Looker, LookML, pipelines Silver/Gold
- [ ] Visão de negócio + dados (raro em engenheiros)
- [ ] Case real e complexo (The Coffee): franquias, royalties, clustering, metas
- [ ] Salário que cobre o básico (você pode falhar sem catástrofe)
- [ ] 35 anos de contexto de mercado (não é ingenuidade)

---

## Roadmap: 12 Semanas

```
Semana 0     │  PREPARAÇÃO    │  Ferramentas + credenciais + case study
Semanas 1-2  │  DESCOBERTA    │  Pesquisa manual + scraping como acelerador
Semanas 3-4  │  VALIDAÇÃO     │  Cold outreach + 5-7 calls com leads
Semanas 5-6  │  PROTOTIPAGEM  │  MVP para 1 nicho escolhido
Semanas 7-8  │  VENDA         │  Primeira consultoria paga
Semanas 9-12 │  APRENDIZADO   │  Iterar, documentar, repetir
```

---

## SEMANA 0 — Preparação (antes de começar o cronômetro)

### Objetivo
Ter tudo pronto para não perder tempo com setup nas semanas pagas.

### Checklist

#### Ferramentas
- [ ] Importar `templates/planilha_sinais_dor.csv` no Google Sheets (sua central de pesquisa)
- [ ] Configurar Calendly com slot de 15 min ("Call de Descoberta — Gratuita")
- [ ] Criar email com assinatura profissional: nome, cargo, link LinkedIn, Calendly

#### Perfil LinkedIn
- [ ] Headline: `Data Engineer → Ajudo [nicho] a transformar dados dispersos em decisões claras`
- [ ] About: 3 parágrafos — problema que você resolve, como você resolve, quem você é
- [ ] Featured: adicionar 1 post sobre The Coffee (quando pronto) ou insight de dados

#### Case Study — The Coffee (seu maior ativo)
- [ ] Escrever documento de 1-2 páginas com estrutura:
  - Contexto (sem nome real): "Rede de franquias, X lojas, setor food service"
  - Problema: sem visibilidade centralizada de performance por loja
  - Solução: pipeline Silver/Gold + dashboard de clusters + ranking de lojas
  - Resultado: qual decisão ficou mais fácil? Qual dado antes era cego?
- [ ] Salvar como PDF e link no Google Drive (para compartilhar nas calls)

#### Infraestrutura de scraping
- [ ] Criar app Reddit em https://www.reddit.com/prefs/apps
- [ ] Preencher `scraper/.env` com credenciais (seguir `scraper/README_scraper.md`)
- [ ] Rodar `pip install -r scraper/requirements.txt`
- [ ] Testar com `python scraper/reddit_scraper.py` para confirmar que funciona

---

## FASE 1 — Descoberta (Semanas 1-2)

### Objetivo
Identificar 1 nicho com dor real, recorrente e disposição de pagar.

### Nichos candidatos (começar com 3)
- [ ] **E-commerce** (Shopify + Google Ads + Meta Ads sem unificação de dados)
- [ ] **SaaS startups** (crescimento rápido, dados espalhados em 10+ ferramentas)
- [ ] **Franquias/redes de lojas** (seu case natural — The Coffee como template)

---

### Semana 1 — Pesquisa Manual (~3-4h total)

**Por que manual primeiro?** Mais rápido para calibrar o que é sinal real de dor. O script da Semana 2 escala o que você já entende.

#### Reddit (manual)
Buscar diretamente em cada subreddit:
- [ ] `r/ecommerce` — prioridade alta
- [ ] `r/shopify` — prioridade alta
- [ ] `r/SaaS` — prioridade alta
- [ ] `r/startups`
- [ ] `r/analytics`
- [ ] `r/dataengineering`
- [ ] `r/businessintelligence`

Queries a usar na busca:
- `"we can't see"` + `data`
- `"we're spending too much"` + `analytics`
- `"pipeline broke"`
- `"can't track"` + `revenue`
- `"data mess"`
- `"too many tools"`
- `"nobody knows where the data is"`
- `"manually exporting"` + `data`
- `"stuck in spreadsheets"`

Anotar na planilha: pelo menos **20-25 sinais** ao final da Semana 1.

#### Product Hunt (manual, ~30 min)
- [ ] Reviews negativos de: Segment, Fivetran, Metabase, Supermetrics, Redash, Airbyte
- [ ] Pergunta-chave: qual problema prometia resolver? Por que o review é negativo?
- [ ] Anotar: dor que o produto não resolveu → oportunidade de consultoria

#### LinkedIn (manual, ~30 min)
- [ ] Busca avançada por posts com:
  - `"data is a mess"`
  - `"can't trust our numbers"`
  - `"analytics is broken"`
  - `"we need someone to"`
- [ ] Salvar: perfil + problema mencionado + link na aba "Leads" da planilha

#### Pesquisa Competitiva (~1h — nova tarefa)
Entender quem mais resolve isso e como se posicionam:
- [ ] Buscar no Upwork: `BigQuery consultant`, `data pipeline freelancer`, `BI dashboard`
  - Anotar: preço médio, como descrevem o serviço, quais dores destacam
- [ ] Buscar no LinkedIn: `data engineering freelancer` + `data consultant`
  - Anotar: como se posicionam, que nicho atendem, que resultado prometem
- [ ] Conclusão: qual gap de posicionamento você pode preencher?

---

### Semana 2 — Escalar com Script (~3-4h total)

- [ ] Rodar `python scraper/reddit_scraper.py` (configurado na Semana 0)
- [ ] Importar CSV gerado na aba "Sinais de Dor" do Google Sheets
- [ ] Remover duplicatas com pesquisa manual
- [ ] Completar até **50+ sinais** no total
- [ ] Preencher aba "Resumo por Nicho" na planilha
- [ ] Decidir: **qual nicho avançar para Fase 2?** (maior frequência + maior intensidade de dor)

### Deliverable da Fase 1
- [ ] Spreadsheet com **50+ sinais de dor**
  - Colunas: Fonte | Nicho | Problema descrito | Link | Intensidade (1-5) | Disposição de pagar? | Data | Status
- [ ] **1 nicho prioritário** escolhido com justificativa documentada
- [ ] Visão inicial dos competidores (preço, posicionamento, gap)

---

## FASE 2 — Validação (Semanas 3-4)

### Objetivo
Falar com pessoas reais. Aprender, não vender.

### Cold Outreach Template

**Subject:** Visto que você mencionou problema com [X dados]

```
Olá [Nome],

Vi que você mencionou dificuldade com [problema específico].

Trabalho há anos com pipelines de dados em BigQuery e especializo 
em centralizar fontes como [Shopify + Ads + CRM] em dashboards 
automáticos que reduzem custo e aumentam visibilidade.

Você toparia uma call de 15 minutos? Sem venda — quero entender 
melhor o seu cenário e ver se consigo ajudar.

Abraço,
Guilherme
```

> **Regra de ouro:** Personalizar os primeiros 2 parágrafos com o problema EXATO da pessoa.

### Checklist de cada call de validação
- [ ] Gravar ou anotar (com permissão)
- [ ] Perguntar: "Me conta como você atualmente [resolve o problema]?"
- [ ] Perguntar: "Quanto tempo/dinheiro você perde com isso por mês?"
- [ ] Perguntar: "Já tentou resolver antes? Por que não funcionou?"
- [ ] Perguntar: "Se eu resolvesse isso, o que seria diferente na sua operação?"
- [ ] **NÃO** apresentar solução ainda — só ouvir
- [ ] Finalizar: "Você pagaria por uma solução? Quanto faz sentido?"
- [ ] Anotar na aba "Calls de Validação" da planilha imediatamente após

### Meta da Fase 2
- [ ] Realizar **5-7 calls**
- [ ] Identificar **padrão de dor comum** entre pelo menos 3 pessoas
- [ ] Ter ao menos **2-3 leads quentes** (disseram que pagariam)

### Deliverable da Fase 2 — Problem Brief (novo)
Além das calls, escrever um documento de 1 página:

```
PROBLEM BRIEF — [Nicho Escolhido]

Nicho: ___________________________________
Dor principal (em palavras exatas dos prospects):
"_______________________________________________"

Dor secundária:
"_______________________________________________"

Objeções mais comuns ouvidas:
1. ___________________________________________
2. ___________________________________________

ROI que o cliente enxerga (o que melhora na operação):
___________________________________________________

Conclusão: vale construir MVP? [ ] Sim  [ ] Não  [ ] Precisa de mais dados
```

> Este documento vira a base da proposta comercial na Fase 4.

---

## FASE 3 — Prototipagem (Semanas 5-6)

### Objetivo
Construir a solução mínima que resolve o problema validado.

### MVP para nicho E-commerce (exemplo)

**Problema:** Shopify + Google Ads + Meta Ads sem dados unificados.  
**Solução:** Pipeline que centraliza tudo em BigQuery + 3 dashboards essenciais.

#### Componentes técnicos
- [ ] Conexão via API: Shopify (pedidos, produtos, clientes)
- [ ] Conexão via API: Google Ads (spend, conversões, ROAS)
- [ ] Conexão via API: Meta Ads (spend, CPC, CPM)
- [ ] Camada Silver no BigQuery (limpeza + deduplicação)
- [ ] Camada Gold no BigQuery (fact tables unificadas)
- [ ] Dashboard Looker Studio: Visão executiva (3 KPIs principais)
- [ ] Dashboard Looker Studio: Análise de campanhas (performance por canal)
- [ ] Dashboard Looker Studio: Vendas por produto/SKU

#### Critérios de "pronto"
- [ ] Funciona sem intervenção manual após setup inicial
- [ ] Atualiza automaticamente (scheduled queries ou Datastream)
- [ ] Documentação básica de 1 página para o cliente
- [ ] Tempo de entrega: máximo 2 semanas de trabalho real

### MVP para nicho Franquias (seu caso natural)

**Problema:** Rede de franquias sem visibilidade centralizada de performance por loja.  
**Solução:** Pipeline medalhão + dashboard de clusters de performance.

- [ ] Adaptar arquitetura The Coffee (Silver/Gold) para modelo genérico
- [ ] Criar template parametrizável por rede (multi-tenant básico)
- [ ] Dashboard: Ranking de lojas, clusters, ticket médio, adoção digital

---

## FASE 4 — Primeira Venda (Semanas 7-8)

### Objetivo
Fechar primeiro contrato de consultoria. Gerar receita real.

### Pacote de Entrada (posicionamento)

```
Data Foundation Package

Inclui:
  ✔ Diagnóstico completo do ambiente de dados (2h)
  ✔ Pipeline customizado com fontes do cliente (5 dias)
  ✔ 3 dashboards operacionais (Looker Studio)
  ✔ Documentação técnica + handoff
  ✔ 30 dias de suporte pós-entrega

Preço: USD $3.000 – $6.000
(ou R$ 15.000 – 30.000 para clientes BR)
```

> **Por que em dólar?** Mercado global, cliente BR paga em real. Mas precificar em USD abre Upwork, LinkedIn global e LatAm.

### Checklist para fechar a venda
- [ ] Enviar proposta simples em PDF (1 página: problema → solução → preço → prazo)
- [ ] Definir forma de pagamento: 50% entrada + 50% na entrega
- [ ] Contrato simples: escopo claro, o que está e o que NÃO está incluído
- [ ] Definir canal de comunicação (Slack, WhatsApp, e-mail)
- [ ] Estabelecer critérios de aceite (o que significa "pronto")

### Objeções comuns e como responder (novo)

| Objeção | Resposta |
|---------|----------|
| "Está caro" | Calcule juntos: quantas horas/mês são perdidas com dados manuais × custo/hora → mostre o payback |
| "Preciso pensar" | "Entendo. Posso oferecer um diagnóstico gratuito de 30 min antes — você decide com mais clareza" |
| "Já tentamos e não funcionou" | "O que você tentou? O que não funcionou?" → identificar gap → mostrar como seu approach é diferente |
| "Não temos budget agora" | Propor escopo reduzido: só o diagnóstico + 1 dashboard por R$5.000, ou retainer mensal menor |
| "Você tem referências?" | Usar o case study The Coffee (anonimizado) + oferecer contato com ex-cliente se possível |

---

## FASE 5 — Iteração e Escala (Semanas 9-12)

### Objetivo
Aprender com o primeiro cliente. Identificar o que pode virar produto.

### Perguntas a responder ao final do primeiro projeto
- [ ] Qual parte levou mais tempo do que deveria? → Automatizar
- [ ] O que o cliente mais valorizou? → Dobrar aposta nisso
- [ ] O que o cliente pediu que não estava no escopo? → Próximo pacote
- [ ] Qual foi o ROI mensurável para o cliente? → Usar como case
- [ ] Daria pra replicar isso para outro cliente com 50% menos esforço? → Caminho para SaaS

### Próximos pacotes (evolução natural)
```
Nível 1 (Atual):     Data Foundation Package    │ $3k-6k por projeto
Nível 2 (Mês 3-6):   Data Retainer              │ $1k-2k/mês (manutenção + evolução)
Nível 3 (Mês 6-12):  Template SaaS              │ $200-500/mês por cliente (self-serve)
```

---

## Métricas de Sucesso (por fase)

| Fase | Métrica | Meta |
|------|---------|------|
| Preparação | Case study pronto | 1 documento |
| Descoberta | Sinais de dor coletados | 50+ |
| Validação | Calls realizadas | 5-7 |
| Validação | Leads quentes identificados | 2-3 |
| Validação | Problem Brief escrito | 1 documento |
| Prototipagem | Dias para entregar MVP | ≤ 14 dias |
| Venda | Contratos fechados | 1 |
| Venda | Receita gerada | ≥ R$ 10.000 |
| Iteração | NPS do cliente | ≥ 8/10 |
| Iteração | Segundo projeto | 1 referral ou recontrato |

---

## Posicionamento & Mensagem

### Para o mercado (como você se apresenta)
> *"Ajudo empresas de e-commerce e redes de franquias a transformarem dados espalhados em decisões claras — com pipelines automatizados, dashboards executivos e uma arquitetura que escala junto com o negócio."*

### Para você mesmo (quando bater medo)
> *"Eu já faço isso. Todo dia. Só estou cobrando por isso de outras pessoas."*

---

## Anti-padrões (o que NÃO fazer)

- [ ] Construir sem validar ("Build it and they will come" — não vêm)
- [ ] Esperar o produto estar perfeito para vender
- [ ] Oferecer "tudo que o cliente pedir" sem escopo definido
- [ ] Trabalhar de graça pra "ganhar experiência" (você já tem experiência)
- [ ] Comparar seu início com o meio do jogo de outra pessoa
- [ ] Colocar mais "não sei" do que "vou aprender"
- [ ] Esperar inspiração. Começar gera inspiração.

---

## Stack Técnica do Projeto

### Data Engineering (seu domínio)
- BigQuery (armazenamento, transformação, scheduled queries)
- Datastream / APIs REST (ingestão)
- SQL (CTEs, Window Functions, MERGE, deduplicação)
- Arquitetura Medalhão (Bronze → Silver → Gold)

### BI & Visualização
- Looker Studio (dashboards executivos para clientes)
- Looker Pro / LookML (para clientes com necessidade de drill-down)

### Automação & Scraping
- Python (PRAW para Reddit, requests, pandas)
- `scraper/reddit_scraper.py` — pronto para uso na Semana 2
- Google Sheets para armazenar e analisar leads

### Venda & Marketing
- LinkedIn (posts 1x/semana sobre problema que você resolve)
- Email simples (Gmail com assinatura profissional)
- Proposta em PDF (Notion, Canva ou Google Docs)
- Calendly (para agendar calls sem fricção)

---

## LinkedIn Content Calendar (novo)

Cadência: **1 post/semana**, atrelado ao que você está aprendendo.

| Semanas | Tema |
|---------|------|
| 1-2 | "O problema que [nicho] tem com dados" — baseado na pesquisa de dor |
| 3-4 | "O que aprendi conversando com X founders sobre dados" |
| 5-6 | "Como construo um pipeline de dados para [resultado] em [prazo]" |
| 7-8 | Bastidores da primeira venda (sem revelar cliente) |
| 9-12 | Resultados reais, case studies anonimizados, aprendizados |

> Formato que converte melhor no LinkedIn: história curta (problema real) → insight → o que você faria diferente. Sem listicles genéricos.

---

## Ritual Semanal

```
Segunda-feira (30 min):  Revisar métricas da semana + ajustar prioridades
Quarta-feira (2h):       Trabalho técnico (scraping, MVP, documentação)
Sexta-feira (1h):        Outreach (3-5 mensagens personalizadas) + 1 post LinkedIn
Domingo (15 min):        Reflexão: o que aprendi? O que trava? O que muda?
```

---

## Checkpoints Críticos

| Data | Checkpoint | Decisão se não atingir |
|------|------------|----------------------|
| Semana 0 | Case study pronto + ferramentas configuradas | Não avançar sem isso |
| Semana 2 | Ter 50+ sinais de dor coletados | Ampliar fontes de busca |
| Semana 4 | Ter feito 5+ calls + Problem Brief escrito | Revisar canal de outreach |
| Semana 6 | MVP funcional entregue | Simplificar escopo |
| Semana 8 | Primeiro contrato fechado | Revisar posicionamento e preço |
| Semana 12 | Avaliação geral do projeto | Continuar, pivotar ou pausar |

---

## Frase para o Espelho

> *"Você tem 35 anos, expertise real, estabilidade financeira e tempo.  
> O risco real é chegar aos 40 e perceber que nunca tentou.  
> Comece feio. Aprenda rápido. Melhore sempre."*

---

*Última atualização: Maio 2026 — Versão 2.0*  
*Próxima revisão: ao final da Semana 2*
