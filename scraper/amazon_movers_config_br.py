CATEGORIES = [
    {
        "name": "Casa e Cozinha",
        "url": "https://www.amazon.com.br/gp/movers-and-shakers/casa/",
        "keyword": "amazon_br_movers_casa_cozinha",
        "amazon_multiplier": 7.0,
    },
    {
        "name": "Pets",
        "url": "https://www.amazon.com.br/gp/movers-and-shakers/pet-supplies/",
        "keyword": "amazon_br_movers_pets",
        "amazon_multiplier": 7.0,
    },
    {
        "name": "Esportes",
        "url": "https://www.amazon.com.br/gp/movers-and-shakers/esportes/",
        "keyword": "amazon_br_movers_esportes",
        "amazon_multiplier": 6.5,
    },
    {
        "name": "Ferramentas",
        "url": "https://www.amazon.com.br/gp/movers-and-shakers/ferramentas/",
        "keyword": "amazon_br_movers_ferramentas",
        "amazon_multiplier": 6.0,
    },
    {
        "name": "Beleza",
        "url": "https://www.amazon.com.br/gp/movers-and-shakers/beleza/",
        "keyword": "amazon_br_movers_beleza",
        "amazon_multiplier": 7.5,
    },
    {
        "name": "Moda",
        "url": "https://www.amazon.com.br/gp/movers-and-shakers/moda/",
        "keyword": "amazon_br_movers_moda",
        "amazon_multiplier": 7.0,
    },
]

# Taxa Amazon BR (~15% referral + estimativa envio)
AMAZON_FEE_PCT = 0.22

# Mínimos para incluir um produto
# BR tem menos reviews em geral — limiar menor
MIN_REVIEWS = 20
MIN_MARGIN_PCT = 25

# Preço máximo em R$ (evita produtos de alto ticket fora do escopo)
MAX_AMAZON_PRICE = 2000.0

# Top N movers por categoria
MAX_PRODUCTS_PER_CATEGORY = 20
