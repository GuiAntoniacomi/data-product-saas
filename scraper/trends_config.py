PRODUCT_SUBREDDITS = {
    "Casa e Cozinha": ["BuyItForLife", "shutupandtakemymoney", "malelivingspace"],
    "Ferramentas": ["HomeImprovement", "DIY"],
    "Jardim": ["gardening"],
    "Fitness": ["fitness", "bodyweightfitness"],
    "Pets": ["dogs", "Pets"],
    "Moda Masculina": ["frugalmalefashion"],
}

PRODUCT_QUERIES = [
    "best product recommend",
    "worth buying love",
    "game changer obsessed",
    "looking for recommend",
    "what do you use",
]

GOOGLE_TREND_KEYWORDS = [
    "kitchen gadget",
    "fitness equipment home",
    "garden tool",
    "home organizer",
]

LEAD_TIME_DAYS = {
    "reddit": 7,
    "google_trends": 14,
}

MIN_REDDIT_SCORE = 10
REDDIT_SEARCH_LIMIT = 20
REDDIT_TIME_FILTER = "month"
MAX_REDDIT_SIGNALS = 60
MAX_TREND_SIGNALS = 30
