"""Salva o HTML da pagina de busca do AliExpress para inspecionar os seletores."""
import asyncio
from playwright.async_api import async_playwright

STEALTH = """
    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
    Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
    Object.defineProperty(navigator, 'languages', {get: () => ['en-US','en']});
    Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
    Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
    window.chrome = {runtime: {}};
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled", "--disable-dev-shm-usage"],
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            locale="en-US",
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"},
        )
        await context.add_init_script(STEALTH)
        page = await context.new_page()

        print("Visitando home...")
        await page.goto("https://www.aliexpress.com/", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(2000)

        url = "https://www.aliexpress.com/wholesale?SearchText=kitchen+organizer&SortType=total_tranpro_desc"
        print(f"Abrindo busca: {url}")
        await page.goto(url, wait_until="networkidle", timeout=45000)
        await page.wait_for_timeout(4000)

        html = await page.content()
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(html)
        print(f"HTML salvo ({len(html)} chars)")

        import re
        title = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        print("Titulo:", title.group(1)[:150] if title else "nao encontrado")

        blocked = any(kw in html.lower() for kw in ['captcha', 'baxia', 'punish', 'robot'])
        print("Bloqueado por bot-check:", blocked)

        selectors = [
            'a[href*="/item/"]',
            '[class*="product"]',
            '[class*="item"]',
            '[class*="card"]',
            '[class*="list"]',
            'div[data-spm]',
        ]
        for sel in selectors:
            els = await page.query_selector_all(sel)
            print(f"  {sel!r:40s} -> {len(els)} elementos")

        await browser.close()

asyncio.run(main())
