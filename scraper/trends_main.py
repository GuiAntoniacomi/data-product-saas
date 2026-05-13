"""
Orquestrador do Módulo 1B — Tendências Emergentes.

Uso:
    python trends_main.py                           # roda Reddit + Google Trends
    python trends_main.py --job-id <uuid>           # atualiza status no Supabase
    python trends_main.py --sources reddit          # filtra fontes
    python trends_main.py --sources google_trends   # só Google Trends
"""

import argparse
from datetime import datetime, timezone

from trends_reddit_scraper import scrape_product_signals
from google_trends_scraper import scrape_trend_signals
from trends_llm import extract_opportunities
from db import update_job, save_trends


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-id", help="ID do job no Supabase para atualizar status")
    parser.add_argument("--sources", default="reddit,google_trends", help="Fontes separadas por vírgula")
    return parser.parse_args()


def run(job_id: str | None, sources: list[str]):
    if job_id:
        update_job(job_id, status="running", started_at=datetime.now(timezone.utc).isoformat())

    all_opportunities = []

    if "reddit" in sources:
        print("\n[Reddit] Coletando sinais de produto...")
        try:
            raw_posts = scrape_product_signals()
            if raw_posts:
                print("[Reddit] Analisando com LLM...")
                opps = extract_opportunities(raw_posts, source="reddit")
                for o in opps:
                    o["source"] = "reddit"
                    o["lead_time_days"] = 7
                all_opportunities.extend(opps)
        except Exception as e:
            print(f"[Reddit] Erro: {e}")

    if "google_trends" in sources:
        print("\n[Google Trends] Coletando sinais...")
        try:
            raw_trends = scrape_trend_signals()
            if raw_trends:
                print("[Google Trends] Analisando com LLM...")
                opps = extract_opportunities(raw_trends, source="google_trends")
                for o in opps:
                    o["source"] = "google_trends"
                    o["lead_time_days"] = 14
                all_opportunities.extend(opps)
        except Exception as e:
            print(f"[Google Trends] Erro: {e}")

    print(f"\nTotal: {len(all_opportunities)} oportunidade(s) encontrada(s)")

    if all_opportunities:
        save_trends(all_opportunities)
        print("Dados salvos no Supabase.")

    if job_id:
        update_job(
            job_id,
            status="completed",
            products_found=len(all_opportunities),
            completed_at=datetime.now(timezone.utc).isoformat(),
        )


if __name__ == "__main__":
    args = parse_args()
    sources = [s.strip() for s in args.sources.split(",")]
    run(args.job_id, sources)
