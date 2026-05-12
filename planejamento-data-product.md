# 🛒 Plano de Negócio — Dropshipping → Private Label → SaaS
> Documento de planejamento e checklist gerado a partir do brainstorming inicial.
> Última atualização: Maio 2026 — v6 (Estratégia de progressão Dropshipping → FBA definida)

---

## 🟢 Status Atual — Maio 2026

### O que foi construído (Semana 0)

| Item | Status | Detalhe |
|------|--------|---------|
| App web base (Next.js 16) | ✅ Feito | Full-stack, App Router, TypeScript |
| Autenticação (Supabase Auth) | ✅ Feito | Login/cadastro, proteção de rotas |
| Banco de dados (Supabase) | ✅ Feito | `ts_product_cache` + `ts_scraper_jobs` |
| Deploy (Vercel) | ✅ Feito | Projeto "Vantis" — `ivuqqezhzhcjwzcakcmm` |
| Repositório GitHub | ✅ Feito | `GuiAntoniacomi/data-product-saas` |
| Scraper AliExpress (Playwright) | ✅ Feito | 5 categorias, filtros de qualidade |
| Score de oportunidade | ✅ Feito | Margem 40% + Pedidos 30% + Reviews 20% + Rating 10% |
| Estimativa de preço Amazon | ✅ Feito | Multiplicador por categoria (3.4×–4.2×) — sem Keepa |
| Botão "Executar Scraper" no app | ✅ Feito | Job assíncrono com polling de status |
| GitHub Actions cron diário | ✅ Feito | 8h Brasília (11:00 UTC) |
| Dashboard de produtos com filtros | ✅ Feito | Busca, categoria, margem mínima |
| Dependências instaladas | ✅ Feito | Playwright Chromium + httpx + beautifulsoup4 |

### Pendente para validar Módulo 1A
- [ ] Adicionar `SUPABASE_URL` e `SUPABASE_SERVICE_ROLE_KEY` nos GitHub Secrets
- [ ] Implementar scraper Amazon Movers & Shakers (ver decisão abaixo)
- [ ] Avaliar qualidade dos produtos encontrados vs. critérios reais de negócio

### Decisão de arquitetura — Fonte de dados do Módulo 1A

**Problema:** O AliExpress bloqueia 100% das tentativas de scraping (headless Playwright, httpx, mobile endpoint) via sistema anti-bot Baxia. Nenhuma abordagem sem autenticação funciona a partir de IP residencial brasileiro.

**Decisão tomada:** Trocar a fonte para **Amazon Movers & Shakers** (Opção B).

**Por que funciona melhor:**
- Páginas públicas da Amazon (`amazon.com/gp/movers-and-shakers/<categoria>/`) são acessíveis sem autenticação
- Dá **preços Amazon reais** em vez de estimativas por multiplicador
- Mostra produtos com demanda comprovada e em crescimento
- Lógica invertida: `preço_aliexpress_estimado = amazon_price / multiplicador_categoria`

**O que muda no scraper:**
- `aliexpress_scraper.py` → substituir por `amazon_movers_scraper.py`
- Campos `aliexpress_price` passam a ser estimativas (ao invés de `estimated_amazon_price`)
- URL do produto aponta para Amazon em vez de AliExpress
- O usuário busca o fornecedor no AliExpress manualmente a partir do produto identificado

**Alternativa futura (Opção A):** AliExpress Affiliate API — cadastro gratuito em portals.aliexpress.com — pode ser implementada depois para cruzar dados de fornecedor com os produtos identificados via Amazon.

---

## 🗺️ Visão Geral da Estratégia

O plano está dividido em **três fases sequenciais**:

| Fase | Modelo | Objetivo | Canal |
|------|--------|----------|-------|
| **Fase 1A** | Dropshipping AliExpress (China) | Entrada com capital mínimo | Amazon |
| **Fase 1B** | FBA Arbitrage (fornecedores americanos) | Margem maior + entrega Prime | Amazon FBA |
| **Fase 2** | Private Label (marca própria com branding) | Construir ativo de marca escalável | Shopify + Instagram/TikTok |
| **Fase 3** | SaaS (vender as ferramentas que construímos) | Receita recorrente de alta margem | App Web B2B para vendedores |

> 💡 **A lógica do ecossistema:** A Fase 1 é a pesquisa de mercado paga para a Fase 2. As ferramentas que você usa na Fase 1 e 2 se tornam o produto da Fase 3. Cada fase financia e valida a próxima.

> 🎓 **Dropshipping é a escola. FBA é o negócio.** Os primeiros 60–90 dias com AliExpress existem para aprender o processo e testar o app com risco mínimo — não para enricar. Quando o app estiver confiável e o primeiro caixa gerado, migrar para FBA onde a margem e a sustentabilidade são reais.

> 🐾 **Princípio Dogfooding:** O SaaS será construído para uso próprio desde o primeiro dia — não como scripts locais que depois viram produto, mas já como app web real. Você usa a ferramenta para rodar o dropshipping, valida a estratégia de negócio e valida o produto simultaneamente, com o mesmo esforço.

---

## 📦 FASE 1 — Vender na Amazon (Dois Modelos Paralelos)

### Modelo 1A — Dropshipping AliExpress (China)
- Produto genérico chinês comprado no AliExpress
- Vendido na Amazon sem estoque físico
- Quando o pedido entra → compra automática no AliExpress no endereço do cliente
- **Capital inicial:** $50–200
- **Prazo de entrega:** 2–4 semanas (ponto fraco)
- **Margem típica:** 10–30%

```
AliExpress (fornecedor)
    → Motor de descoberta (Módulo 1A + 1B)
        → Listing na Amazon
            → Pedido do cliente
                → Compra automática no AliExpress
                    → Entrega direta ao cliente (sem estoque)
```

---

### Modelo 1B — FBA Arbitrage (Fornecedores Americanos)
Comprar produtos em liquidação/atacado nos EUA, mandar para um **Prep Center** que etiqueta e prepara, e deixar a Amazon entregar via Prime (1–2 dias).

Três variantes dentro desse modelo:

| Variante | Como funciona | Escalabilidade |
|---|---|---|
| **Retail Arbitrage** | Compra promoções em Walmart/Target/Costco fisicamente | Baixa — depende de você caçando oferta |
| **Online Arbitrage** | Mesma lógica mas em lojas online, automatizável | Média — dá para escanear com software |
| **Wholesale** | Compra direto do distribuidor/fabricante em volume | Alta — modelo mais sustentável |

**Pipeline FBA:**
```
Scanner de oportunidades (nosso Módulo 1A adaptado)
    → Fornecedor americano (Walmart, liquidadores, distribuidores)
        → Prep Center (embala + etiqueta no padrão Amazon FBA) ← $1–3/unidade
            → Amazon FBA (armazém da Amazon)
                → Cliente compra
                    → Amazon entrega (Prime 1–2 dias) ← vantagem enorme
```

**Exemplo real (visto em vídeo):**
| Dado | Valor |
|---|---|
| Produto | Camisa polo Callaway (liquidação) |
| BSR | 23k — top 1% da categoria |
| Vendas estimadas | $568/mês |
| Custo de compra | $9,00 |
| Preço de venda Amazon | $32,90 |
| Lucro líquido/unidade | $9,99 |
| Margem | 30% |
| ROI | 111% |

---

### Comparativo dos dois modelos:

| | Dropshipping AliExpress | FBA Arbitrage (EUA) |
|---|---|---|
| Capital inicial | $50–200 | $300–1.000 |
| Prazo de entrega | 2–4 semanas | 1–2 dias (Prime) |
| Margem típica | 10–30% | 20–50% |
| Controle de qualidade | Baixo | Alto |
| Risco de suspensão Amazon | Alto | Baixo |
| Automação possível | Alta | Média |
| Melhor para começar | ✅ Capital mínimo | ✅ Margem e credibilidade |

> 🗺️ **Estratégia de progressão definida:**
> - **Mês 1–3:** Dropshipping AliExpress — aprender o processo, testar o app, errar barato. Meta: primeiros $200–500 em vendas.
> - **Mês 3–6:** Migrar para FBA Arbitrage com o caixa gerado — margem real, entrega Prime, negócio sustentável.
> - **Mês 6+:** Escalar FBA + iniciar Private Label com produtos validados pelo app.

---

### 💰 Custos reais de entrada (sem enganação):

**Modelo 1A — Dropshipping AliExpress:**
| Item | Custo |
|---|---|
| Amazon Seller Account (Individual) | Gratuito até 40 vendas/mês |
| Amazon Seller Account (Professional) | $39,99/mês |
| Primeiro lote de testes (5–10 produtos) | $50–150 |
| Ferramentas de pesquisa (Keepa básico) | $19/mês |
| **Total para começar** | **~$100–250** |

**Modelo 1B — FBA Arbitrage:**
| Item | Custo |
|---|---|
| Amazon Seller Account Professional | $39,99/mês |
| Prep Center (por unidade enviada) | $1–3/unidade |
| Frete fornecedor → Prep Center | $5–15/envio |
| Taxa FBA da Amazon | $3–6/unidade |
| Endereço virtual nos EUA (se necessário) | $10–30/mês |
| Estoque inicial (20–50 unidades) | $200–500 |
| **Total para começar com seriedade** | **~$400–800** |

> ⚠️ **Sobre o "R$100 para começar":** É marketing de curso. Cobre talvez a primeira compra, mas não as taxas fixas, prep center e margem de segurança. Entre com expectativa real para não desistir no primeiro mês.

---

## 🛠️ FERRAMENTAS A CONSTRUIR

### 🔍 Módulo 1A — Motor de Descoberta de Produtos (Mercado Atual)
**Objetivo:** Identificar automaticamente produtos com boa margem e demanda real já consolidada. Funciona para **ambos os modelos** — AliExpress (dropshipping) e arbitrage doméstico (FBA).

#### Checklist de funcionalidades:
**Para Dropshipping AliExpress:**
- [x] ~~Conexão com AliExpress Affiliate API~~ → **Scraper Playwright** (sem API paga)
- [x] Scraper de produtos mais vendidos por categoria (5 categorias: Casa, Pets, Fitness, Jardim, Ferramentas)
- [x] Coleta de: preço do fornecedor, reviews, volume de vendas, rating
- [x] ~~Keepa / Rainforest API~~ → **Estimativa por multiplicador de categoria** (3.4×–4.2×) — sem custo
- [x] Cálculo automático de margem: `(amazon_est - ali - taxa_amazon) / amazon_est`
- [x] Filtro configurável no dashboard: margem mínima, categoria, busca por nome
- [x] Score de oportunidade: `margem×40% + pedidos×30% + reviews×20% + rating×10%`
- [x] Dashboard web com tabela de produtos ordenada por score
- [ ] Validação real: confirmar que os produtos encontrados têm demanda real na Amazon

**Para FBA Arbitrage (fornecedores americanos):**
- [ ] Scanner de preços em lojas americanas (Walmart, Target, liquidadores online)
- [ ] Comparação automática: preço da loja × preço Amazon atual
- [ ] Cálculo de margem FBA: custo compra + prep center ($2) + taxa FBA + margem Amazon
- [ ] Exibir: BSR, vendas estimadas/mês, número de vendedores FBA concorrentes, ROI
- [ ] Inspiração: replicar o painel do Seller Amp (BSR, Est. Sales, Cost Price, Sale Price, Profit%, ROI)

---

### 🧠 Módulo 1B — Inteligência de Tendências Emergentes
**Objetivo:** Detectar produtos com demanda crescente *antes* que a concorrência chegue. Enquanto o Módulo 1A olha o que já vende, este olha o que **vai vender**.

#### Por que isso é vantagem competitiva:
```
Tendência surge em cultura/mídia        ← 1B entra AQUI
    → Vira busca no Google/TikTok       ← 1B entra AQUI
        → Vira pedido no AliExpress
            → Vira produto ranqueado na Amazon
                → Concorrência explode  ← Módulo 1A já é tarde
```

#### Fontes de sinal monitoradas:
| Fonte | O que captura | Antecedência |
|-------|--------------|--------------|
| **TikTok** (#TikTokMadeMeBuyIt, trending products) | Viral orgânico, impulso de compra imediato | 1–7 dias |
| **Reddit** (r/BuyItForLife, r/LifeProTips, r/malelivingspace, r/frugal) | Necessidade real articulada por consumidores | 7–30 dias |
| **Google Trends** | Curva de busca ascendente sem oferta consolidada | 7–30 dias |
| **Pinterest Trends** | Forte para casa, decoração, moda, beleza | 14–60 dias |
| **Amazon Movers & Shakers** | Produtos que mais subiram no ranking nas últimas 24h | 1–3 dias |
| **AliExpress New Arrivals** | Fornecedor apostando em produto novo com reviews crescendo | 30–90 dias |

#### Arquitetura do agente:
```
Crawlers por fonte (TikTok + Reddit + Google Trends + Pinterest + Amazon M&S)
    → LLM analisa padrões: frequência de menção, sentimento, intenção de compra
        → Extrai: nome do produto, categoria, problema que resolve
            → Cruza com AliExpress: "esse produto existe? qual o preço?"
                → Cruza com Amazon: "quantos vendedores? reviews? concorrência?"
                    → Score de oportunidade:
                        alta demanda emergente + baixa oferta = 🟢 OPORTUNIDADE
                        alta demanda + alta oferta = 🔴 TARDE DEMAIS
```

#### Checklist de funcionalidades:
- [ ] Monitor de hashtags e produtos virais no **TikTok API** ou scraper
- [ ] Leitor de posts e comentários relevantes no **Reddit API (PRAW)**
- [ ] Monitor de termos no **Google Trends API (pytrends)**
- [ ] Monitor de **Pinterest Trends**
- [ ] Scraper diário do **Amazon Movers & Shakers** por categoria
- [ ] Monitor de **AliExpress New Arrivals** com crescimento de reviews
- [ ] LLM para consolidar sinais e extrair nomes de produtos acionáveis
- [ ] Cruzamento automático: sinal de tendência → busca no AliExpress → busca na Amazon
- [ ] Score composto: `(força do sinal × antecedência) / (nº de concorrentes na Amazon)`
- [ ] Alerta diário com top 5 oportunidades emergentes
- [ ] Histórico de tendências para aprendizado: quais sinais previram bem?

---

### 📝 Módulo 2 — Publicador de Listings na Amazon
**Objetivo:** Criar e publicar anúncios na Amazon de forma automatizada.

#### Checklist de funcionalidades:
- [ ] Integração com **Amazon SP-API**
- [ ] Criação de listing com: título, descrição, bullet points, fotos
- [ ] Uso de **LLM para otimizar copy** (título SEO-friendly, descrição persuasiva)
- [ ] Download automático de imagens do produto do AliExpress
- [ ] Publicação em categoria correta
- [ ] Monitoramento de status do listing (ativo, suspenso, etc.)

---

### 🤖 Módulo 3 — Agente de Fulfillment Automático
**Objetivo:** Quando um pedido entra na Amazon, comprar automaticamente no AliExpress.

#### Checklist de funcionalidades:
- [ ] Listener de novos pedidos na Amazon SP-API
- [ ] Trigger automático de compra no AliExpress com endereço do cliente
- [ ] Mapeamento produto Amazon → produto AliExpress (evitar compra errada)
- [ ] Atualização do código de rastreamento no pedido Amazon
- [ ] Alerta em caso de falha na compra ou produto fora de estoque

---

### 💬 Módulo 4 — Agente de Atendimento ao Cliente
**Objetivo:** Responder dúvidas de clientes automaticamente via Amazon.

#### Checklist de funcionalidades:
- [ ] Integração com mensagens do Amazon Seller Central
- [ ] LLM treinado com contexto dos produtos vendidos
- [ ] Respostas automáticas para perguntas comuns: prazo de entrega, status do pedido, trocas
- [ ] Escalação para humano quando necessário
- [ ] Monitoramento de reviews negativos para resposta rápida

---

### 📊 Módulo 5 — Dashboard de Performance
**Objetivo:** Visão unificada do negócio para tomada de decisão.

#### Checklist de funcionalidades:
- [ ] Receita por produto e por período
- [ ] Margem líquida por SKU
- [ ] Taxa de reembolso e reclamações
- [ ] Produtos com queda de ranking → sinal de substituição
- [ ] Alertas de margem comprimida (ex: concorrente baixou preço)

---

## 🏗️ FASE 2 — Private Label (Marca Própria)

### Conceito
Produto genérico chinês + branding forte + storytelling = margem de 10x.
A diferença não é o produto, é a **percepção de valor**.

### Pipeline
```
Produto genérico AliExpress (identificado na Fase 1)
    → Nome de marca própria
        → Identidade visual premium (logo, embalagem, paleta)
            → Copy com storytelling
                → Shopify (site próprio)
                    → Instagram/TikTok como vitrine
                        → Amazon como canal secundário
```

### O que torna a Fase 1 essencial para a Fase 2:
- Você vai saber **quais categorias têm demanda real**
- Vai saber **o que os clientes reclamam nos reviews** → oportunidade de melhorar
- O motor de descoberta vai identificar **produtos com alto volume mas sem vendedor com marca forte** → esse é o gap para entrar com branding

### Checklist Fase 2 (futuro):
- [ ] Definir nicho e produto campeão (validado na Fase 1)
- [ ] Criar identidade de marca (nome, logo, paleta, tom de voz)
- [ ] Montar Shopify com design premium
- [ ] Produzir conteúdo para Instagram/TikTok
- [ ] Negociar com fornecedor chinês para personalização de embalagem (MOQ mínimo)
- [ ] Estratégia de lançamento com influenciadores de nicho

---

## 💻 FASE 3 — SaaS (A Ferramenta como Produto)

### Conceito
Tudo que construímos nas Fases 1 e 2 para uso próprio vira um **produto vendável para outros vendedores**. Você sai de usuário da ferramenta para dono da ferramenta.

### Por que é o modelo mais lucrativo dos três:

| | Dropshipping | Private Label | SaaS |
|---|---|---|---|
| Margem líquida | 5–20% | 40–60% | 70–90% |
| Escalabilidade | Linear | Média | Exponencial |
| Risco operacional | Alto | Médio | Baixo |
| Ativo gerado | Nenhum | Marca | Produto recorrente |
| 1000 clientes pagantes | Muito trabalho | Muito estoque | Mesmo custo de infra |

### Competidores e onde nos diferenciamos:

| Ferramenta | Preço/mês | Ponto fraco |
|---|---|---|
| Jungle Scout | ~$49 | Foco só em dados históricos da Amazon |
| Helium 10 | ~$99 | Complexo, caro, sem detecção de tendências emergentes |
| Zik Analytics | ~$29 | Foco em eBay, fraco em tendências |
| **Nossa ferramenta** | **A definir** | **Módulo 1B — tendências via TikTok, Reddit, Google Trends — gap real do mercado** |

### De scripts locais para produto SaaS:

```
HOJE (scripts locais)             FASE 3 (produto SaaS)
─────────────────────             ──────────────────────
Script Python rodando local   →   Backend em nuvem (AWS / GCP)
Resultado no terminal         →   Dashboard web com UI limpa
1 usuário (você)              →   Multi-tenant (N usuários)
Gratuito                      →   Assinatura mensal em USD
Configuração manual           →   Onboarding guiado
```

### Stack técnica real (atualizado em Mai/2026):

- **Full-stack:** Next.js 16 (App Router) — unifica frontend + backend, sem FastAPI separado
- **Estilo:** Tailwind CSS + dark theme (zinc/violet)
- **Banco:** Supabase (PostgreSQL gerenciado + Auth + RLS por usuário)
- **Scraper:** Python + Playwright (headless Chromium, assíncrono)
- **Comunicação scraper → DB:** httpx direto na REST API do Supabase (service role)
- **Jobs:** assíncrono via `spawn` detached no Next.js + polling via Supabase
- **Agendamento:** GitHub Actions cron (diário 8h Brasília)
- **Pagamentos:** Stripe (a implementar na Fase 3)
- **Deploy:** Vercel (app) — repositório `GuiAntoniacomi/data-product-saas`

### Planos sugeridos (a validar com mercado):

| Plano | Preço/mês | O que inclui |
|---|---|---|
| **Starter** | ~$19 | Módulo 1A — produtos consolidados, 50 buscas/dia |
| **Growth** | ~$49 | 1A + 1B — tendências emergentes + alertas diários |
| **Pro** | ~$99 | Tudo + publicador de listings + agente de fulfillment |

### Checklist Fase 3:
- [ ] Refatorar scripts locais em API REST (FastAPI)
- [ ] Construir autenticação e sistema de planos por tier
- [ ] Construir frontend web — dashboard de oportunidades de produtos
- [ ] Integrar Stripe para cobrança recorrente em USD
- [ ] Sistema multi-tenant (cada usuário vê só seus dados)
- [ ] Onboarding guiado (conectar conta Amazon, configurar categorias de interesse)
- [ ] Landing page com posicionamento claro vs. Jungle Scout e Helium 10
- [ ] Estratégia de aquisição: comunidades de dropshipping no Reddit, YouTube, TikTok
- [ ] Programa de afiliados para escalar sem anúncio pago

---

## 📋 CHECKLIST DE CONTAS E ACESSOS NECESSÁRIOS

### Para começar — Modelo 1A (Dropshipping AliExpress):
- [ ] **Amazon Seller Account** (Individual gratuito para começar)
- [ ] **AliExpress Affiliate Account** (para acesso à API oficial)
- [ ] **Keepa** ou **Rainforest API** (pesquisa de preços Amazon)
- [ ] Conta bancária / Payoneer para receber pagamentos da Amazon em USD

### Para começar — Modelo 1B (FBA Arbitrage):
- [ ] **Amazon Seller Account Professional** ($39,99/mês)
- [ ] Conta em um **Prep Center americano** (ShipBob, Prep It Pack It Ship It, etc.)
- [ ] **Endereço virtual nos EUA** se necessário (Earth Class Mail, Anytime Mailbox)
- [ ] **Payoneer ou Wise** para receber em USD e pagar fornecedores americanos
- [ ] Acesso a liquidadores online: **BULQ, Direct Liquidation, Amazon Liquidations**

### Para escalar (Fase 2):
- [ ] **Amazon Brand Registry** (necessário para Private Label)
- [ ] **Shopify** (Fase 2)
- [ ] **Meta Business / TikTok Ads** (Fase 2)

### Para o SaaS (Fase 3):
- [ ] **Stripe** (pagamentos recorrentes em USD)
- [x] **Supabase** (banco de dados + autenticação) — projeto Vantis ativo
- [x] **Vercel** (deploy do app Next.js)
- [x] **GitHub** (repositório + Actions para cron) — `GuiAntoniacomi/data-product-saas`
- [ ] Domínio próprio para o produto

---

## ⚠️ RISCOS CONHECIDOS E MITIGAÇÕES

| Risco | Impacto | Fase | Mitigação |
|-------|---------|------|-----------|
| Suspensão de conta Amazon | Alto | 1 e 2 | Seguir políticas à risca, começar com volume baixo |
| Margem comprimida por concorrência | Médio | 1 | Motor de score monitorando concorrentes continuamente |
| Fornecedor sem estoque após pedido | Alto | 1 | Agente de fulfillment com fallback e alerta imediato |
| Produto bloqueado por regulação | Médio | 1 | Evitar categorias sensíveis (cosméticos, eletrônicos) |
| Prazo de entrega longo (China → EUA) | Alto | 1 | Priorizar fornecedores com armazém nos EUA no AliExpress |
| Concorrente copiar o produto da marca | Médio | 2 | Registrar marca (trademark) nos EUA via USPTO |
| Churn alto no SaaS por falta de diferencial | Alto | 3 | Módulo 1B é o diferencial — proteger e evoluir continuamente |
| Bloqueio de API (TikTok, Reddit) | Médio | 3 | Múltiplas fontes de sinal — nunca depender de uma só |
| App construído sem uso real → features erradas | Alto | 3 | Mitigado pelo dogfooding — você usa antes de vender |

---

## 🚀 ORDEM DE EXECUÇÃO RECOMENDADA

**— PRÉ-FASE: Infraestrutura do App (base de tudo) —**
```
1. Criar conta Amazon Seller (Individual — gratuito)
2. ✅ Construir o app web base — já como SaaS desde o início:
   - ✅ Frontend web (Next.js 16 + Tailwind)
   - ✅ Backend (API Routes no Next.js — sem FastAPI separado)
   - ✅ Autenticação (Supabase)
   - ✅ Deploy (Vercel)
   - ✅ Scraper Python + Playwright com trigger pelo app
   → Você é o primeiro e único usuário nessa etapa
```

**— FASE 1A: Escola — Dropshipping AliExpress (Mês 1–3) —**
> Objetivo: aprender o processo e validar o app. Não é para enricar — é para errar barato.
```
3.  🔄 Construir Módulo 1A no app (Motor de Descoberta AliExpress)
    ✅ Scraper AliExpress, score, dashboard — pendente: validação com dados reais
4.  Construir Módulo 1B no app (Tendências Emergentes)
5.  Usar o app para descobrir produtos e publicar na Amazon manualmente
6.  Validar: os produtos que o app recomenda realmente vendem?
7.  Refinar score e sinais com base nos resultados reais
8.  Construir Módulo 3 no app (Fulfillment Automático AliExpress)
9.  Construir Módulo 4 no app (Atendimento ao Cliente com LLM)
    → Meta: primeiros $200–500 em vendas, app funcionando e confiável
```

**— FASE 1B: Negócio — FBA Arbitrage (Mês 3–6) —**
> Objetivo: migrar para o modelo sustentável com o caixa e conhecimento da Fase 1A.
```
10. Abrir conta Amazon Seller Professional ($39,99/mês)
11. Contratar Prep Center americano
12. Adaptar Módulo 1A para escanear fornecedores americanos (BSR, ROI, FBA fees)
13. Primeiras compras de arbitrage — Online Arbitrage para escalar
14. Construir Módulo 2 no app (Publicador de Listings — agora com dados FBA)
15. Construir Módulo 5 no app (Dashboard — margem FBA, BSR, giro de estoque)
    → Meta: primeiros $1.000–3.000/mês em vendas FBA
```

**— FASE 2: Construir Marca — Private Label (Mês 6+) —**
```
16. Usar o app para identificar produto campeão com gap de branding
17. Criar identidade de marca e montar Shopify
18. Produzir conteúdo e lançar com influenciadores de nicho
```

**— FASE 3: Abrir o SaaS para outros usuários —**
```
19. App validado em produção real por você durante meses
20. Adicionar Stripe (cobrança recorrente em USD)
21. Criar planos de preço e sistema multi-tenant
22. Lançar em comunidades de dropshipping (Reddit, YouTube, TikTok)
23. Programa de afiliados para crescimento orgânico
```

> ⚡ **Módulo 1A vs 1B:** O 1A (produtos consolidados) garante resultado imediato. O 1B (tendências emergentes) é a vantagem competitiva — você publica antes da concorrência.

> 💰 **Dropshipping vs FBA:** Dropshipping é a escola — capital mínimo, aprendizado máximo. FBA é o negócio — margem real, entrega Prime, sustentável. Um financia e prepara o outro.

> 🏆 **O ativo final é o SaaS:** O dropshipping e o private label pagam as contas. O SaaS é o ativo de longo prazo — você vira dono da pá, não apenas garimpeiro.

> 🎯 **Princípio guia:** Entender o processo manual antes de automatizar. Vender 1–2 produtos na mão primeiro. A automação resolve dores reais que você viveu, não problemas imaginados.
