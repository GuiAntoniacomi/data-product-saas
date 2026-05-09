SUBREDDITS_BY_NICHE = {
    "E-commerce": [
        "ecommerce",
        "shopify",
        "Entrepreneur",
    ],
    "SaaS": [
        "SaaS",
        "startups",
        "analytics",
    ],
    "Franquias": [
        "franchise",
        "smallbusiness",
    ],
    "Geral": [
        "dataengineering",
        "businessintelligence",
    ],
}

PAIN_QUERIES = [
    "we can't see our data",
    "data is a mess",
    "can't track revenue",
    "pipeline broke",
    "too many tools analytics",
    "data scattered everywhere",
    "need someone to clean our data",
    "analytics is broken",
    "can't trust our numbers",
    "reporting is a nightmare",
    "no visibility into",
    "manually exporting data",
    "stuck in spreadsheets",
    "we're flying blind",
    "nobody knows where the data is",
]

# Maps subreddit name → niche label
NICHE_MAP = {
    "ecommerce": "E-commerce",
    "shopify": "E-commerce",
    "Entrepreneur": "E-commerce",
    "SaaS": "SaaS",
    "startups": "SaaS",
    "analytics": "SaaS",
    "franchise": "Franquias",
    "smallbusiness": "Franquias",
    "dataengineering": "Geral",
    "businessintelligence": "Geral",
}

# Minimum Reddit score to include a post (filter noise)
MIN_SCORE = 2

# How far back to search
TIME_FILTER = "year"  # options: hour, day, week, month, year, all

# Max posts per (subreddit, query) combination
SEARCH_LIMIT = 30
