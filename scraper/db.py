import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

_client: Client | None = None


def get_client() -> Client:
    global _client
    if _client is None:
        url = os.environ["SUPABASE_URL"]
        key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
        _client = create_client(url, key)
    return _client


def update_job(job_id: str, **fields):
    get_client().table("ts_scraper_jobs").update(fields).eq("id", job_id).execute()


def save_products(products: list[dict]):
    if not products:
        return
    # Limpa cache antigo das mesmas keywords antes de inserir
    keywords = list({p["search_keyword"] for p in products})
    get_client().table("ts_product_cache").delete().in_("search_keyword", keywords).execute()
    get_client().table("ts_product_cache").insert(products).execute()
