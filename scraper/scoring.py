def calculate_margin(aliexpress_price: float, amazon_multiplier: float, amazon_fee_pct: float) -> tuple[float, float]:
    """Retorna (estimated_amazon_price, margin_pct)."""
    amazon_price = round(aliexpress_price * amazon_multiplier, 2)
    amazon_fee = amazon_price * amazon_fee_pct
    profit = amazon_price - aliexpress_price - amazon_fee
    margin_pct = int((profit / amazon_price) * 100)
    return amazon_price, margin_pct


def calculate_score(margin_pct: int, monthly_orders: int, reviews_count: int, rating: float) -> int:
    """Score 0-100 baseado em margem, volume e qualidade."""
    # Normaliza cada dimensão para 0-100
    margin_score = min(margin_pct * 2, 100)           # 50% margem = 100pts
    orders_score = min(monthly_orders / 50, 100)       # 5000 pedidos/mês = 100pts
    reviews_score = min(reviews_count / 20, 100)       # 2000 reviews = 100pts
    rating_score = max((rating - 3.0) / 2.0 * 100, 0) # 5.0 estrelas = 100pts

    score = int(
        margin_score * 0.40 +
        orders_score * 0.30 +
        reviews_score * 0.20 +
        rating_score * 0.10
    )
    return min(score, 100)
