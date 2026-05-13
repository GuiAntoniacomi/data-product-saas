import os
import httpx
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

_headers: dict | None = None
_base_url: str | None = None


def _get(url: str, headers: dict) -> tuple[str, dict]:
    return url, headers


def _init():
    global _headers, _base_url
    if _headers is None:
        url = os.environ["SUPABASE_URL"]
        key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
        _base_url = f"{url}/rest/v1"
        _headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        }


def update_job(job_id: str, **fields):
    _init()
    httpx.patch(
        f"{_base_url}/ts_scraper_jobs",
        headers=_headers,
        params={"id": f"eq.{job_id}"},
        json=fields,
    ).raise_for_status()


def save_products(products: list[dict]):
    if not products:
        return
    _init()
    keywords = list({p["search_keyword"] for p in products})
    quoted = ",".join(f'"{k}"' for k in keywords)
    httpx.delete(
        f"{_base_url}/ts_product_cache",
        headers=_headers,
        params={"search_keyword": f"in.({quoted})"},
    ).raise_for_status()
    httpx.post(
        f"{_base_url}/ts_product_cache",
        headers={**_headers, "Prefer": "return=minimal"},
        json=products,
    ).raise_for_status()


def save_trends(trends: list[dict]):
    if not trends:
        return
    _init()
    try:
        httpx.delete(
            f"{_base_url}/ts_trend_signals",
            headers=_headers,
            params={"source": "in.(reddit,google_trends)"},
        ).raise_for_status()
    except Exception as e:
        print(f"  Aviso: limpeza de trends falhou ({e}), inserindo mesmo assim")
    httpx.post(
        f"{_base_url}/ts_trend_signals",
        headers={**_headers, "Prefer": "return=minimal"},
        json=trends,
    ).raise_for_status()
