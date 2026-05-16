"""
Scraper do Amazon Movers & Shakers.

Lógica invertida em relação ao scraper AliExpress:
  amazon_price   = preço REAL coletado da página
  supplier_price = amazon_price / multiplier  (estimativa custo do fornecedor)
  margin         = (amazon_price - supplier_price - taxa_amazon) / amazon_price

Campos de saída:
  aliexpress_price      → custo estimado do fornecedor
  aliexpress_url        → URL do produto na Amazon
  estimated_amazon_price → preço real da Amazon
  monthly_orders        → proxy: rank_change_pct * 10 (ex: 200% → 2000)
  marketplace           → 'amazon_us' | 'amazon_br'
"""

import asyncio
import re
from playwright.async_api import async_playwright

from amazon_movers_config import (
    CATEGORIES, AMAZON_FEE_PCT,
    MIN_REVIEWS, MIN_MARGIN_PCT, MAX_PRODUCTS_PER_CATEGORY,
)
from scoring import calculate_score

_STEALTH = """
    Object.defineProperty(navigator, 'webdriver',          {get: () => undefined});
    Object.defineProperty(navigator, 'plugins',            {get: () => [1,2,3,4,5]});
    Object.defineProperty(navigator, 'languages',          {get: () => ['en-US','en']});
    Object.defineProperty(navigator, 'platform',           {get: () => 'Win32'});
    Object.defineProperty(navigator, 'hardwareConcurrency',{get: () => 8});
    window.chrome = {runtime: {}};
"""

_BLOCK_KEYWORDS = [
    "captcha", "robot check", "automated access", "type the characters",
    "verificação", "robô", "acesso automatizado",
]


# ── helpers ───────────────────────────────────────────────────────────────────

def _price(text: str, is_br: bool = False) -> float:
    text = (text or "").strip()
    if is_br:
        # R$ 1.299,99 → 1299.99  (period = thousands, comma = decimal in BR)
        text = re.sub(r"[^\d.,]", "", text)
        text = text.replace(".", "").replace(",", ".")
    else:
        text = text.replace(",", "")
    m = re.search(r"[\d]+\.?\d*", text)
    try:
        return float(m.group()) if m else 0.0
    except ValueError:
        return 0.0


def _int(text: str) -> int:
    """'7,782' ou '1 ratings' → 7782."""
    cleaned = re.sub(r"[^\d]", "", text or "")
    return int(cleaned) if cleaned else 0


def _pct(text: str) -> float:
    """'169%' → 169.0"""
    m = re.search(r"[\d.]+", text or "")
    try:
        return float(m.group()) if m else 0.0
    except ValueError:
        return 0.0


def _parse_aria_stars(label: str) -> tuple[float, int]:
    """
    EN: '4.5 out of 5 stars, 7,782 ratings' → (4.5, 7782)
    PT: '4,5 de 5 estrelas, 1.234 avaliações' → (4.5, 1234)
    """
    rating, reviews = 0.0, 0

    # Português
    m_r = re.search(r"([\d,]+)\s+de\s+5", label or "")
    if m_r:
        try:
            rating = float(m_r.group(1).replace(",", "."))
        except ValueError:
            pass
    m_n = re.search(r"([\d.,]+)\s+avalia", label or "")
    if m_n:
        reviews = _int(m_n.group(1))

    # Inglês (fallback — Amazon BR frequentemente usa inglês no HTML)
    if not rating:
        m_r = re.search(r"([\d.]+)\s+out of 5", label or "")
        if m_r:
            try:
                rating = float(m_r.group(1))
            except ValueError:
                pass
    if not reviews:
        m_n = re.search(r"([\d,]+)\s+rating", label or "")
        if m_n:
            reviews = _int(m_n.group(1))

    return rating, reviews


# ── item parser ───────────────────────────────────────────────────────────────

async def _parse_item(
    item,
    rank_pos: int,
    category: str,
    keyword: str,
    multiplier: float,
    marketplace: str,
    fee_pct: float,
    min_reviews: int,
    min_margin: int,
    max_products: int,
    max_price: float,
) -> dict | None:
    is_br = marketplace == "amazon_br"
    base_url = "https://www.amazon.com.br" if is_br else "https://www.amazon.com"

    # ── Título ────────────────────────────────────────────────────────────────
    title_el = await item.query_selector("[class*='p13n-sc-css-line-clamp']")
    if not title_el:
        title_el = await item.query_selector("[class*='p13n-sc-truncate']")
    title = (await title_el.inner_text()).strip() if title_el else ""
    if not title or len(title) < 5:
        return None

    # ── Preço real Amazon ────────────────────────────────────────────────────
    price_el = await item.query_selector("[class*='p13n-sc-price']")
    price_text = (await price_el.inner_text()).strip() if price_el else ""
    amazon_price = _price(price_text, is_br=is_br)
    if amazon_price <= 0 or amazon_price > max_price:
        return None

    # ── Rating + reviews (via aria-label do link de estrelas) ────────────────
    stars_a = await item.query_selector("a[aria-label*='stars']")
    if not stars_a:
        stars_a = await item.query_selector("a[aria-label*='estrelas']")
    rating, reviews_count = 0.0, 0
    if stars_a:
        label = await stars_a.get_attribute("aria-label") or ""
        rating, reviews_count = _parse_aria_stars(label)
    if rating == 0.0:
        alt_el = await item.query_selector("span.a-icon-alt")
        if alt_el:
            alt_text = await alt_el.inner_text()
            m = re.search(r"([\d.]+)", alt_text)
            if m:
                try:
                    rating = float(m.group(1))
                except ValueError:
                    pass
    if rating == 0.0:
        rating = 4.0

    if reviews_count < min_reviews:
        return None

    # ── URL do produto ────────────────────────────────────────────────────────
    url_el = await item.query_selector("a.a-link-normal[role='link']")
    if not url_el:
        url_el = await item.query_selector("a.aok-block[href*='/dp/']")
    if not url_el:
        url_el = await item.query_selector("a[href*='/dp/']")
    href = (await url_el.get_attribute("href") or "") if url_el else ""
    if href.startswith("/"):
        href = f"{base_url}{href}"
    href = href.split("?")[0]

    # ── Imagem ────────────────────────────────────────────────────────────────
    img_el = await item.query_selector("img.a-dynamic-image")
    if not img_el:
        img_el = await item.query_selector("img[class*='p13n-product-image']")
    if not img_el:
        img_el = await item.query_selector("img")
    img_url = ""
    if img_el:
        img_url = await img_el.get_attribute("src") or ""
        if img_url.startswith("data:"):
            img_url = await img_el.get_attribute("data-src") or ""

    # ── Rank change % (o sinal central do M&S) ───────────────────────────────
    pct_el = await item.query_selector("span.zg-grid-pct-change")
    pct_text = (await pct_el.inner_text()).strip() if pct_el else ""
    rank_change_pct = _pct(pct_text)

    # ── Custo estimado do fornecedor (lógica invertida) ───────────────────────
    supplier_price = round(amazon_price / multiplier, 2)

    # ── Margem ────────────────────────────────────────────────────────────────
    amazon_fee = amazon_price * fee_pct
    profit = amazon_price - supplier_price - amazon_fee
    margin_pct = int((profit / amazon_price) * 100) if amazon_price > 0 else 0
    if margin_pct < min_margin:
        return None

    # ── Proxy de demanda ──────────────────────────────────────────────────────
    if rank_change_pct > 0:
        monthly_orders_proxy = int(rank_change_pct * 10)
    else:
        monthly_orders_proxy = max(150, (max_products + 1 - rank_pos) * 150)

    score = calculate_score(margin_pct, monthly_orders_proxy, reviews_count, rating)

    return {
        "name": title[:200],
        "aliexpress_price": supplier_price,
        "aliexpress_url": href,
        "aliexpress_img": img_url,
        "estimated_amazon_price": amazon_price,
        "margin_pct": margin_pct,
        "monthly_orders": monthly_orders_proxy,
        "reviews_count": reviews_count,
        "rating": rating,
        "score": score,
        "category": category,
        "search_keyword": keyword,
        "marketplace": marketplace,
    }


# ── category scraper ──────────────────────────────────────────────────────────

async def _scrape_category(page, category: dict, config: dict, marketplace: str) -> list[dict]:
    name = category["name"]
    url = category["url"]
    multiplier = category["amazon_multiplier"]
    keyword = category["keyword"]

    print(f"  [{marketplace}][{name}] {url}")

    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=45000)
        await page.wait_for_timeout(3000)

        content = await page.content()
        if any(k in content.lower() for k in _BLOCK_KEYWORDS):
            print(f"  [{name}] Bloqueio detectado — pulando.")
            return []

        items = await page.query_selector_all("div.p13n-grid-content")
        if not items:
            items = await page.query_selector_all("div[id^='p13n-asin-index-']")

        if not items:
            print(f"  [{name}] Nenhum item encontrado.")
            return []

        print(f"  [{name}] {len(items)} itens na página.")

        products = []
        for rank_pos, item in enumerate(items[:config["max_products"]], start=1):
            try:
                product = await _parse_item(
                    item, rank_pos, name, keyword, multiplier, marketplace,
                    fee_pct=config["fee_pct"],
                    min_reviews=config["min_reviews"],
                    min_margin=config["min_margin"],
                    max_products=config["max_products"],
                    max_price=config["max_price"],
                )
                if product:
                    products.append(product)
            except Exception:
                continue

        print(f"  [{name}] {len(products)} produto(s) passaram nos filtros.")
        return products

    except Exception as e:
        print(f"  [{name}] Erro: {e}")
        return []


# ── entry point ───────────────────────────────────────────────────────────────

async def scrape_keywords(categories: list[dict], marketplace: str = "amazon_us") -> list[dict]:
    """
    marketplace: 'amazon_us' | 'amazon_br'
    Compatível com a assinatura usada em main.py.
    """
    is_br = marketplace == "amazon_br"

    # Importa config correto dinamicamente
    if is_br:
        from amazon_movers_config_br import (
            AMAZON_FEE_PCT as FEE,
            MIN_REVIEWS as MR,
            MIN_MARGIN_PCT as MM,
            MAX_PRODUCTS_PER_CATEGORY as MP,
            MAX_AMAZON_PRICE as MAX_P,
        )
    else:
        from amazon_movers_config import (
            AMAZON_FEE_PCT as FEE,
            MIN_REVIEWS as MR,
            MIN_MARGIN_PCT as MM,
            MAX_PRODUCTS_PER_CATEGORY as MP,
        )
        MAX_P = 500.0

    config = {
        "fee_pct": FEE,
        "min_reviews": MR,
        "min_margin": MM,
        "max_products": MP,
        "max_price": MAX_P,
    }

    locale = "pt-BR" if is_br else "en-US"
    accept_lang = "pt-BR,pt;q=0.9" if is_br else "en-US,en;q=0.9"

    all_products = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--disable-gpu",
            ],
        )
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
            locale=locale,
            extra_http_headers={
                "Accept-Language": accept_lang,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            },
        )
        await context.add_init_script(_STEALTH)
        page = await context.new_page()

        for cat in categories:
            products = await _scrape_category(page, cat, config, marketplace)
            all_products.extend(products)
            await asyncio.sleep(3)

        await browser.close()

    return all_products


if __name__ == "__main__":
    results = asyncio.run(scrape_keywords(CATEGORIES, marketplace="amazon_us"))
    print(f"\n{len(results)} produto(s) encontrados\n")
    for prod in sorted(results, key=lambda x: x["score"], reverse=True):
        name = prod["name"][:55].encode("ascii", errors="replace").decode("ascii")
        print(
            f"  {prod['score']:3d} pts | {prod['margin_pct']:2d}% margem | "
            f"${prod['aliexpress_price']:.2f} custo -> ${prod['estimated_amazon_price']:.2f} Amazon | "
            f"rank+{prod['monthly_orders']//10:.0f}% | "
            f"{name}"
        )
