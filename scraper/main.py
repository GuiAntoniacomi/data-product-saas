"""
Orquestrador do scraper Vantis.

Uso:
    python main.py                           # roda US + BR
    python main.py --marketplace us          # só Amazon US
    python main.py --marketplace br          # só Amazon BR
    python main.py --job-id <uuid>           # atualiza status no Supabase
    python main.py --categories "Pets,Fitness"  # filtra categorias (US)
"""

import asyncio
import argparse
import sys
from datetime import datetime, timezone

from amazon_movers_config import CATEGORIES as CATEGORIES_US
from amazon_movers_config_br import CATEGORIES as CATEGORIES_BR
from amazon_movers_scraper import scrape_keywords
from db import update_job, save_products


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-id", help="ID do job no Supabase para atualizar status")
    parser.add_argument("--categories", help="Categorias separadas por vírgula (só Amazon US)")
    parser.add_argument(
        "--marketplace",
        choices=["us", "br", "both"],
        default="both",
        help="Qual marketplace scraper: us, br ou both (padrão: both)",
    )
    return parser.parse_args()


async def run_marketplace(categories: list[dict], marketplace: str) -> list[dict]:
    label = "amazon_us" if marketplace == "us" else "amazon_br"
    print(f"\n=== Iniciando scraper {label.upper()} — {len(categories)} categoria(s) ===")
    products = await scrape_keywords(categories, marketplace=label)
    print(f"  {label}: {len(products)} produto(s) encontrado(s)")
    return products


async def run(job_id: str | None, category_filter: list[str] | None, marketplace: str):
    if job_id:
        update_job(job_id, status="running", started_at=datetime.now(timezone.utc).isoformat())

    all_products = []

    try:
        if marketplace in ("us", "both"):
            cats_us = CATEGORIES_US
            if category_filter:
                cats_us = [c for c in CATEGORIES_US if c["name"] in category_filter]
                if not cats_us:
                    print(f"Nenhuma categoria US encontrada: {category_filter}")
            if cats_us:
                products_us = await run_marketplace(cats_us, "us")
                all_products.extend(products_us)

        if marketplace in ("br", "both"):
            products_br = await run_marketplace(CATEGORIES_BR, "br")
            all_products.extend(products_br)

        print(f"\nTotal geral: {len(all_products)} produto(s)")

        if all_products:
            save_products(all_products)
            print("Dados salvos no Supabase.")

        if job_id:
            update_job(
                job_id,
                status="completed",
                products_found=len(all_products),
                completed_at=datetime.now(timezone.utc).isoformat(),
            )

    except Exception as e:
        print(f"Erro: {e}")
        if job_id:
            update_job(job_id, status="failed", error=str(e))
        raise


if __name__ == "__main__":
    args = parse_args()
    category_filter = [c.strip() for c in args.categories.split(",")] if args.categories else None
    asyncio.run(run(args.job_id, category_filter, args.marketplace))
