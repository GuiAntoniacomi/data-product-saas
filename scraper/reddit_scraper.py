"""
Reddit Pain Signal Scraper
--------------------------
Use na Semana 2 para complementar e escalar a pesquisa manual da Semana 1.
Gera um CSV que você importa direto no Google Sheets.

Pré-requisito: criar app Reddit e preencher .env (veja README_scraper.md)
Uso: python reddit_scraper.py
"""

import os
import sys
import praw
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

from config import (
    SUBREDDITS_BY_NICHE,
    PAIN_QUERIES,
    NICHE_MAP,
    MIN_SCORE,
    TIME_FILTER,
    SEARCH_LIMIT,
)

load_dotenv()

PAYMENT_SIGNALS = [
    "pay", "paying", "paid", "budget", "cost", "expensive",
    "worth it", "hire", "contractor", "freelancer", "consultant",
    "invoice", "quote", "pricing",
]


def get_reddit_client():
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT", "data-pain-scraper/1.0")

    if not client_id or not client_secret:
        print("Erro: REDDIT_CLIENT_ID e REDDIT_CLIENT_SECRET não encontrados no .env")
        print("Consulte o README_scraper.md para criar suas credenciais.")
        sys.exit(1)

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )


def score_pain_intensity(score: int, num_comments: int, text: str) -> int:
    """Heurística de intensidade de dor (1-5) baseada em engajamento + sinais textuais."""
    intensity = 1
    if score > 30 or num_comments > 5:
        intensity = 2
    if score > 100 or num_comments > 20:
        intensity = 3
    if score > 300 or num_comments > 50:
        intensity = 4
    if score > 800 or num_comments > 100:
        intensity = 5
    # Boost se texto contém sinais de disposição de pagar
    if any(s in text.lower() for s in PAYMENT_SIGNALS):
        intensity = min(intensity + 1, 5)
    return intensity


def has_payment_signal(text: str) -> str:
    if any(s in text.lower() for s in PAYMENT_SIGNALS):
        return "S"
    return "?"


def scrape(reddit: praw.Reddit) -> list[dict]:
    results = []
    seen_urls: set[str] = set()

    for niche, subreddits in SUBREDDITS_BY_NICHE.items():
        for subreddit_name in subreddits:
            for query in PAIN_QUERIES:
                print(f"  r/{subreddit_name:<25} | query: {query}")
                try:
                    sub = reddit.subreddit(subreddit_name)
                    posts = sub.search(
                        query,
                        limit=SEARCH_LIMIT,
                        sort="relevance",
                        time_filter=TIME_FILTER,
                    )
                    for post in posts:
                        if post.score < MIN_SCORE:
                            continue
                        url = f"https://reddit.com{post.permalink}"
                        if url in seen_urls:
                            continue
                        seen_urls.add(url)

                        full_text = post.title + " " + (post.selftext or "")

                        results.append({
                            "fonte": "Reddit",
                            "nicho": NICHE_MAP.get(subreddit_name, niche),
                            "problema_descrito": post.title[:300],
                            "link": url,
                            "intensidade_dor": score_pain_intensity(
                                post.score, post.num_comments, full_text
                            ),
                            "tem_disposicao_pagar": has_payment_signal(full_text),
                            "data": datetime.utcfromtimestamp(post.created_utc).strftime("%Y-%m-%d"),
                            "titulo_post": post.title[:150],
                            "score_reddit": post.score,
                            "comentarios_reddit": post.num_comments,
                            "subreddit": subreddit_name,
                            "status": "novo",
                        })

                except Exception as e:
                    print(f"    Erro em r/{subreddit_name}: {e}")

    return results


def save_csv(results: list[dict], output: str = "sinais_de_dor_reddit.csv"):
    if not results:
        print("\nNenhum resultado encontrado. Verifique suas credenciais e tente novamente.")
        return

    df = pd.DataFrame(results)
    df = df.drop_duplicates(subset=["link"])
    df = df.sort_values(["intensidade_dor", "score_reddit"], ascending=[False, False])
    df.to_csv(output, index=False, encoding="utf-8-sig")  # utf-8-sig para abrir no Excel/Sheets sem problema

    print(f"\nArquivo salvo: {output}")
    print(f"Total de sinais: {len(df)}")
    print(f"\nPor nicho:")
    print(df["nicho"].value_counts().to_string())
    print(f"\nTop 5 por intensidade:")
    print(df[["intensidade_dor", "nicho", "titulo_post"]].head(5).to_string(index=False))
    print(f"\nProximo passo: importe '{output}' no Google Sheets e consolide com sua pesquisa manual.")


if __name__ == "__main__":
    print("Reddit Pain Signal Scraper — Semana 2")
    print("=" * 50)
    reddit = get_reddit_client()
    print("Conectado ao Reddit. Iniciando busca...\n")
    results = scrape(reddit)
    save_csv(results)
