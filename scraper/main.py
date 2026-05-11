"""
Orquestrador do scraper Vantis.

Uso:
    python main.py                          # roda todas as categorias
    python main.py --job-id <uuid>          # atualiza status no Supabase
    python main.py --categories "Pets,Fitness"  # filtra categorias
"""

import asyncio
import argparse
import sys
from datetime import datetime, timezone

from aliexpress_config import CATEGORIES
from aliexpress_scraper import scrape_keywords
from db import update_job, save_products


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-id", help="ID do job no Supabase para atualizar status")
    parser.add_argument("--categories", help="Categorias separadas por vírgula")
    return parser.parse_args()


async def run(job_id: str | None, category_filter: list[str] | None):
    categories = CATEGORIES
    if category_filter:
        categories = [c for c in CATEGORIES if c["name"] in category_filter]
        if not categories:
            print(f"Nenhuma categoria encontrada: {category_filter}")
            sys.exit(1)

    if job_id:
        update_job(job_id, status="running", started_at=datetime.now(timezone.utc).isoformat())

    print(f"Iniciando scraper - {len(categories)} categoria(s)")
    try:
        products = await scrape_keywords(categories)
        print(f"\nTotal: {len(products)} produto(s) encontrado(s)")

        if products:
            save_products(products)
            print("Dados salvos no Supabase.")

        if job_id:
            update_job(
                job_id,
                status="completed",
                products_found=len(products),
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
    asyncio.run(run(args.job_id, category_filter))
