import asyncio
import re
from playwright.async_api import async_playwright, Page

from aliexpress_config import MAX_PRODUCTS_PER_KEYWORD, MIN_REVIEWS, MIN_MONTHLY_ORDERS
from scoring import calculate_margin, calculate_score


async def _extract_products(page: Page, keyword: str, category: str,
                             amazon_multiplier: float, amazon_fee_pct: float) -> list[dict]:
    url = f"https://www.aliexpress.com/wholesale?SearchText={keyword.replace(' ', '+')}&SortType=total_tranpro_desc"
    products = []

    try:
        await page.goto(url, wait_until="networkidle", timeout=45000)
        await page.wait_for_timeout(4000)

        # Fecha popup de localização se aparecer
        try:
            await page.click('[class*="close"]', timeout=2000)
        except Exception:
            pass

        items = await page.query_selector_all('[class*="product-snippet"]')
        if not items:
            items = await page.query_selector_all('a[href*="/item/"]')

        for item in items[:MAX_PRODUCTS_PER_KEYWORD * 2]:
            try:
                product = await _parse_item(item, keyword, category, amazon_multiplier, amazon_fee_pct)
                if product:
                    products.append(product)
                if len(products) >= MAX_PRODUCTS_PER_KEYWORD:
                    break
            except Exception:
                continue

    except Exception as e:
        print(f"  [erro] {keyword}: {e}")

    return products


async def _parse_item(item, keyword: str, category: str,
                      amazon_multiplier: float, amazon_fee_pct: float) -> dict | None:
    # Título
    title_el = await item.query_selector('[class*="title"]')
    if not title_el:
        return None
    name = (await title_el.inner_text()).strip()
    if not name or len(name) < 5:
        return None

    # Preço
    price_el = await item.query_selector('[class*="price"]')
    if not price_el:
        return None
    price_text = (await price_el.inner_text()).strip()
    price_match = re.search(r'[\d,.]+', price_text.replace(',', '.'))
    if not price_match:
        return None
    try:
        price = float(price_match.group())
    except ValueError:
        return None
    if price <= 0 or price > 200:
        return None

    # Reviews
    reviews = 0
    reviews_el = await item.query_selector('[class*="review"], [class*="feedback"]')
    if reviews_el:
        rev_text = await reviews_el.inner_text()
        rev_match = re.search(r'[\d,]+', rev_text.replace(',', ''))
        if rev_match:
            try:
                reviews = int(rev_match.group())
            except ValueError:
                pass

    # Rating
    rating = 4.0
    rating_el = await item.query_selector('[class*="star"], [class*="rating"]')
    if rating_el:
        rat_text = await rating_el.inner_text()
        rat_match = re.search(r'[\d.]+', rat_text)
        if rat_match:
            try:
                r = float(rat_match.group())
                if 1.0 <= r <= 5.0:
                    rating = r
            except ValueError:
                pass

    # Pedidos mensais estimados
    orders = 0
    orders_el = await item.query_selector('[class*="order"], [class*="sold"]')
    if orders_el:
        ord_text = await orders_el.inner_text()
        ord_match = re.search(r'[\d,]+', ord_text.replace(',', ''))
        if ord_match:
            try:
                orders = int(ord_match.group())
            except ValueError:
                pass

    # Imagem
    img_url = ""
    img_el = await item.query_selector('img')
    if img_el:
        img_url = await img_el.get_attribute('src') or await img_el.get_attribute('data-src') or ""

    # Link
    link_el = await item.query_selector('a[href*="/item/"]')
    product_url = ""
    if link_el:
        href = await link_el.get_attribute('href') or ""
        product_url = href if href.startswith('http') else f"https:{href}"

    # Filtros mínimos
    if reviews < MIN_REVIEWS or orders < MIN_MONTHLY_ORDERS:
        return None

    amazon_price, margin_pct = calculate_margin(price, amazon_multiplier, amazon_fee_pct)
    score = calculate_score(margin_pct, orders, reviews, rating)

    return {
        "name": name[:200],
        "aliexpress_price": price,
        "aliexpress_url": product_url,
        "aliexpress_img": img_url,
        "estimated_amazon_price": amazon_price,
        "margin_pct": margin_pct,
        "monthly_orders": orders,
        "reviews_count": reviews,
        "rating": rating,
        "score": score,
        "category": category,
        "search_keyword": keyword,
    }


async def scrape_keywords(keywords_by_category: list[dict]) -> list[dict]:
    """Recebe lista de {name, keywords, amazon_multiplier} e retorna todos os produtos."""
    from aliexpress_config import AMAZON_FEE_PCT

    all_products = []

    # Script injetado em cada frame antes de qualquer JS da pagina executar.
    # Mascara as propriedades que o Baxia/AliExpress usa para detectar headless.
    stealth_script = """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US','en']});
        Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
        Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
        window.chrome = {runtime: {}};
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(p) {
            if (p === 37445) return 'Intel Inc.';
            if (p === 37446) return 'Intel Iris OpenGL Engine';
            return getParameter.call(this, p);
        };
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--disable-gpu",
            ]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="en-US",
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            },
        )
        await context.add_init_script(stealth_script)
        page = await context.new_page()

        # Visita a home primeiro para simular sessao real e pegar cookies
        await page.goto("https://www.aliexpress.com/", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(2000)

        for cat in keywords_by_category:
            print(f"  Categoria: {cat['name']}")
            for keyword in cat["keywords"]:
                print(f"    Buscando: {keyword}")
                products = await _extract_products(
                    page, keyword, cat["name"],
                    cat["amazon_multiplier"], AMAZON_FEE_PCT
                )
                print(f"    -> {len(products)} produto(s) encontrado(s)")
                all_products.extend(products)
                await asyncio.sleep(2)  # pausa entre requests

        await browser.close()

    return all_products


if __name__ == "__main__":
    from aliexpress_config import CATEGORIES
    results = asyncio.run(scrape_keywords(CATEGORIES))
    for p in results:
        print(f"{p['score']:3d} | {p['margin_pct']:3d}% | ${p['aliexpress_price']:.2f} -> ${p['estimated_amazon_price']:.2f} | {p['name'][:60]}")
