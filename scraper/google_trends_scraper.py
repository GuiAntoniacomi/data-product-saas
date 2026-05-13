"""
Module 1B — Google Trends Signal Scraper
Collects rising product queries using pytrends (no API key required).
"""

import time
from pytrends.request import TrendReq

from trends_config import GOOGLE_TREND_KEYWORDS, MAX_TREND_SIGNALS


def scrape_trend_signals() -> list[dict]:
    """Collect rising Google Trends queries for product categories."""
    pytrends = TrendReq(hl="en-US", tz=360, timeout=(10, 25))
    results = []
    seen: set[str] = set()

    for keyword in GOOGLE_TREND_KEYWORDS:
        if len(results) >= MAX_TREND_SIGNALS:
            break
        try:
            pytrends.build_payload([keyword], timeframe="today 3-m", geo="US")
            related = pytrends.related_queries()
            rising_df = related.get(keyword, {}).get("rising")

            if rising_df is not None and not rising_df.empty:
                for _, row in rising_df.head(5).iterrows():
                    term = str(row["query"]).strip()
                    if term in seen:
                        continue
                    seen.add(term)
                    value = row["value"]
                    trend_pct = 500 if value == "Breakout" else int(value)
                    results.append({
                        "source": "google_trends",
                        "keyword": term,
                        "base_keyword": keyword,
                        "trend_pct": trend_pct,
                    })
            time.sleep(3)
        except Exception as e:
            print(f"  Erro Google Trends ({keyword}): {e}")
            time.sleep(10)

    print(f"  Google Trends: {len(results)} termos coletados")
    return results
