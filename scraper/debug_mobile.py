"""Investiga o endpoint mobile do AliExpress que nao retornou captcha."""
import httpx, json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Accept": "application/json, text/html, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://m.aliexpress.com/",
}

with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=20) as client:
    # Tenta variações do endpoint mobile
    tests = [
        ("mobile_search_json", "https://m.aliexpress.com/fn/search-pc/index",
         {"SearchText": "kitchen organizer", "page": 1, "pageSize": 10}),

        ("mobile_wholesale", "https://m.aliexpress.com/wholesale",
         {"SearchText": "kitchen organizer", "SortType": "total_tranpro_desc"}),

        ("mobile_w", "https://m.aliexpress.com/w/wholesale-kitchen-organizer.html",
         {}),

        # API de busca usada pelo app mobile
        ("app_search", "https://m.aliexpress.com/fn/search-pc/index",
         {"keywords": "kitchen organizer", "page": 1, "pageSize": 10, "sort": "default"}),
    ]

    for name, url, params in tests:
        try:
            r = client.get(url, params=params)
            body = r.text
            is_captcha = any(kw in body.lower() for kw in ["captcha", "baxia", "punish", "_____tmd_____"])
            has_items = any(kw in body.lower() for kw in ["/item/", "productid", "itemid", "listingid"])

            print(f"\n[{name}]")
            print(f"  status={r.status_code}  len={len(body)}  captcha={is_captcha}  has_items={has_items}")
            print(f"  content-type: {r.headers.get('content-type','?')}")
            if body.strip():
                print(f"  preview: {body[:400]}")
            else:
                print("  (resposta vazia)")
        except Exception as e:
            print(f"\n[{name}] ERRO: {e}")
