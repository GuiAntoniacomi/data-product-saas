"""Testa se a API JSON interna do AliExpress responde sem CAPTCHA."""
import httpx, json, re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.aliexpress.com/",
    "X-Requested-With": "XMLHttpRequest",
}

endpoints = [
    # Endpoint de busca usado pelo site (retorna JSON)
    ("search_fn", "https://www.aliexpress.com/fn/search-pc/index",
     {"SearchText": "kitchen organizer", "SortType": "total_tranpro_desc", "page": 1, "pageSize": 10}),

    # Endpoint alternativo (af/search-by)
    ("search_af", "https://www.aliexpress.com/af/search-by.html",
     {"SearchText": "kitchen organizer", "SortType": "total_tranpro_desc", "initiative_id": "SB_"}),

    # API de produto direto (mobile)
    ("mobile_search", "https://m.aliexpress.com/fn/search-pc/index",
     {"SearchText": "kitchen organizer", "page": 1}),
]

with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=15) as client:
    for name, url, params in endpoints:
        try:
            r = client.get(url, params=params)
            content = r.text[:500]
            is_json = r.headers.get("content-type", "").startswith("application/json")
            is_captcha = "captcha" in r.text.lower() or "baxia" in r.text.lower()
            print(f"\n[{name}] status={r.status_code} json={is_json} captcha={is_captcha}")
            print(f"  URL final: {r.url}")
            print(f"  Primeiros 300 chars: {content[:300]}")
        except Exception as e:
            print(f"\n[{name}] ERRO: {e}")
