"""
Module 1B — Reddit Product Signal Scraper
Uses Reddit's public JSON API — no credentials required.
"""

import time
import httpx

from trends_config import (
    PRODUCT_SUBREDDITS,
    PRODUCT_QUERIES,
    MIN_REDDIT_SCORE,
    REDDIT_SEARCH_LIMIT,
    REDDIT_TIME_FILTER,
    MAX_REDDIT_SIGNALS,
)

_HEADERS = {
    "User-Agent": "vantis-trends/1.0 (product research bot)",
    "Accept": "application/json",
}


def _search_subreddit(client: httpx.Client, subreddit: str, query: str) -> list[dict]:
    try:
        res = client.get(
            f"https://www.reddit.com/r/{subreddit}/search.json",
            params={
                "q": query,
                "sort": "top",
                "t": REDDIT_TIME_FILTER,
                "limit": REDDIT_SEARCH_LIMIT,
                "restrict_sr": 1,
            },
            headers=_HEADERS,
            timeout=15,
        )
        res.raise_for_status()
        return res.json().get("data", {}).get("children", [])
    except Exception as e:
        print(f"  Erro r/{subreddit} ({query}): {e}")
        return []


def scrape_product_signals() -> list[dict]:
    """Collect raw product recommendation posts from subreddits."""
    results = []
    seen_urls: set[str] = set()

    with httpx.Client() as client:
        for category, subreddits in PRODUCT_SUBREDDITS.items():
            if len(results) >= MAX_REDDIT_SIGNALS:
                break
            for subreddit_name in subreddits:
                if len(results) >= MAX_REDDIT_SIGNALS:
                    break
                for query in PRODUCT_QUERIES:
                    if len(results) >= MAX_REDDIT_SIGNALS:
                        break

                    posts = _search_subreddit(client, subreddit_name, query)
                    for child in posts:
                        post = child.get("data", {})
                        if post.get("score", 0) < MIN_REDDIT_SCORE:
                            continue
                        permalink = post.get("permalink", "")
                        url = f"https://reddit.com{permalink}"
                        if url in seen_urls:
                            continue
                        seen_urls.add(url)
                        results.append({
                            "source": "reddit",
                            "category_hint": category,
                            "subreddit": subreddit_name,
                            "title": post.get("title", "")[:300],
                            "body": (post.get("selftext") or "")[:300],
                            "score": post.get("score", 0),
                            "comments": post.get("num_comments", 0),
                            "url": url,
                        })

                    time.sleep(0.5)  # respeitar rate limit público (60 req/min)

    print(f"  Reddit: {len(results)} posts coletados")
    return results
