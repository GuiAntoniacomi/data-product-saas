# 🛒 Plano de Negócio — Dropshipping → Private Label → SaaS
> Documento de planejamento e checklist gerado a partir do brainstorming inicial.
> Última atualização: Maio 2026 — v5 (Semana 0 concluída — app base + Módulo 1A em desenvolvimento)

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
- [ ] Executar scraper pela primeira vez e confirmar produtos no dashboard
- [ ] Avaliar qualidade dos produtos encontrados vs. critérios reais de negócio

---

## 🗺️ Visão Geral da Estratégia

O plano está dividido em **três fases sequenciais**:

| Fase | Modelo | Objetivo | Canal |
|------|--------|----------|-------|
| **Fase 1** | Dropshipping (produto genérico da China) | Gerar caixa + validar as ferramentas | Amazon |
| **Fase 2** | Private Label (marca própria com branding) | Construir ativo de marca escalável | Shopify + Instagram/TikTok |
| **Fase 3** | SaaS (vender as ferramentas que construímos) | Receita recorrente de alta margem | App Web B2B para vendedores |

> 💡 **A lógica do ecossistema:** A Fase 1 é a pesquisa de mercado paga para a Fase 2. As ferramentas que você usa na Fase 1 e 2 se tornam o produto da Fase 3. Cada fase financia e valida a próxima.

> 🐾 **Princípio Dogfooding:** O SaaS será construído para uso próprio desde o primeiro dia — não como scripts locais que depois viram produto, mas já como app web real. Você usa a ferramenta para rodar o dropshipping, valida a estratégia de negócio e valida o produto simultaneamente, com o mesmo esforço.

---

## 📦 FASE 1 — Dropshipping na Amazon

### Conceito
- Produto genérico chinês comprado no AliExpress
- Vendido na Amazon sem estoque físico
- Quando o pedido entra → compra automática no AliExpress no endereço do cliente

### Pipeline completo
```
AliExpress (fornecedor)
    → Motor de descoberta de produtos (scraping/API)
        → Score de viabilidade (margem, ranking, reviews)
            → Listing na Amazon (via SP-API)
                → Pedido do cliente
                    → Compra automática no AliExpress
                        → Entrega ao cliente
```

---

## 🛠️ FERRAMENTAS A CONSTRUIR

### 🔍 Módulo 1A — Motor de Descoberta de Produtos (Mercado Atual)
**Objetivo:** Identificar automaticamente produtos com boa margem e demanda real já consolidada.

#### Checklist de funcionalidades:
- [x] ~~Conexão com AliExpress Affiliate API~~ → **Scraper Playwright** (sem API paga)
- [x] Scraper de produtos mais vendidos por categoria (5 categorias: Casa, Pets, Fitness, Jardim, Ferramentas)
- [x] Coleta de: preço do fornecedor, reviews, volume de vendas, rating
- [x] ~~Keepa / Rainforest API~~ → **Estimativa por multiplicador de categoria** (3.4×–4.2×) — sem custo
- [x] Cálculo automático de margem: `(amazon_est - ali - taxa_amazon) / amazon_est`
- [x] Filtro configurável no dashboard: margem mínima, categoria, busca por nome
- [x] Score de oportunidade: `margem×40% + pedidos×30% + reviews×20% + rating×10%`
- [x] Dashboard web com tabela de produtos ordenada por score
- [ ] Validação real: confirmar que os produtos encontrados têm demanda real na Amazon

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

### Para começar (Fase 1):
- [ ] **Amazon Seller Account** (Individual para começar, Professional quando escalar)
- [ ] **AliExpress Affiliate Account** (para acesso à API oficial)
- [ ] **Keepa** ou **Rainforest API** (pesquisa de preços Amazon)
- [ ] Conta bancária / PayPal para receber pagamentos da Amazon
- [ ] Endereço americano (prep center ou serviço de endereço virtual nos EUA)

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
1. Criar conta Amazon Seller
2. ✅ Construir o app web base — já como SaaS desde o início:
   - ✅ Frontend web (Next.js 16 + Tailwind)
   - ✅ Backend (API Routes no Next.js — sem FastAPI separado)
   - ✅ Autenticação (Supabase)
   - ✅ Deploy (Vercel)
   - ✅ Scraper Python + Playwright com trigger pelo app
   → Você é o primeiro e único usuário nessa etapa
```

**— FASE 1: Gerar Caixa (usando o app) —**
```
3.  🔄 Construir Módulo 1A dentro do app (Motor de Descoberta — produtos consolidados)
    ✅ Scraper AliExpress, score, dashboard — pendente: validação com dados reais
4.  Construir Módulo 1B dentro do app (Tendências Emergentes)
5.  Usar o app para descobrir produtos reais e publicar na Amazon manualmente
6.  Validar: os produtos que o app recomenda realmente vendem?
7.  Refinar o score e sinais com base nos resultados reais
8.  Construir Módulo 2 dentro do app (Publicador de Listings)
9.  Construir Módulo 3 dentro do app (Fulfillment Automático)
10. Construir Módulo 4 dentro do app (Atendimento ao Cliente)
11. Construir Módulo 5 dentro do app (Dashboard de Performance)
```

**— FASE 2: Construir Marca (usando o app para pesquisa) —**
```
12. Usar o app para identificar produto campeão com gap de branding
13. Criar identidade de marca e montar Shopify
14. Produzir conteúdo e lançar com influenciadores de nicho
```

**— FASE 3: Abrir o SaaS para outros usuários —**
```
15. App já está pronto e validado em produção real (você mesmo usou)
16. Adicionar Stripe (cobrança recorrente em USD)
17. Criar planos de preço e sistema multi-tenant
18. Lançar em comunidades de dropshipping (Reddit, YouTube, TikTok)
19. Programa de afiliados para crescimento orgânico
```

> ⚡ **1A vs 1B:** O 1A garante receita no curto prazo com produtos validados. O 1B é a vantagem competitiva — produtos publicados antes de todo mundo.

> 💰 **Fases 1+2 vs Fase 3:** O dropshipping e o private label pagam as contas. O SaaS é o ativo de longo prazo — você vira dono da pá, não apenas garimpeiro.

> 🎯 **Princípio guia:** Entender o processo manual antes de automatizar. Vender 1–2 produtos na mão primeiro. A automação resolve dores reais que você viveu, não problemas imaginados.
