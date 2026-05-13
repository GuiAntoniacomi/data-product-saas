"""
Module 1B — LLM Product Opportunity Extractor
Uses Claude Haiku to extract product opportunities from raw signals.
"""

import os
import json
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()

CATEGORIES = ["Casa e Cozinha", "Ferramentas", "Fitness", "Pets", "Jardim", "Moda Masculina"]

_REDDIT_PROMPT = """\
You are a product research analyst for an Amazon dropshipping business (US market).

Analyze these Reddit posts from product recommendation communities and identify the TOP physical product opportunities.
Focus on: specific products mentioned, products people are actively looking for, products with strong praise or demand.
Skip: services, software, digital products, food, supplements, brand-only items with no generic equivalent.

For each product opportunity, return:
- product_name: specific English product name (e.g. "Cordless Tire Inflator", "Bamboo Stand-Up Weed Puller")
- category: MUST be one of [{categories}]
- opportunity_score: 0-100 (demand clarity + purchase intent + dropshipping viability)
- trend_strength: 0-100 (based on upvotes + comments engagement)
- signal_text: key phrase from the post revealing this opportunity (max 150 chars)
- source_url: the Reddit URL from the data
- subreddit: subreddit name

Reddit posts:
{signals}

Return ONLY a valid JSON array. Maximum 15 items. No markdown, no explanation."""

_GOOGLE_PROMPT = """\
You are a product research analyst for an Amazon dropshipping business (US market).

These are rising Google search queries in the US. Identify which represent physical product purchase opportunities.
Skip: services, questions without product intent, food, brand-only queries.

For each product opportunity, return:
- product_name: specific English product name or type
- category: MUST be one of [{categories}]
- opportunity_score: 0-100 (purchase intent clarity + dropshipping viability)
- trend_strength: use the % value provided (max 500 for Breakout)
- signal_text: the exact search query
- source_url: null
- subreddit: null

Rising queries:
{signals}

Return ONLY a valid JSON array. Maximum 10 items. No markdown, no explanation."""


def extract_opportunities(signals: list[dict], source: str) -> list[dict]:
    """Send raw signals to Claude Haiku and extract product opportunities."""
    if not signals:
        return []

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    cats = ", ".join(CATEGORIES)

    if source == "reddit":
        top_signals = sorted(signals, key=lambda s: s.get("score", 0), reverse=True)[:40]
        signals_text = "\n".join(
            f"[r/{s['subreddit']}] score:{s['score']} | {s['title'][:120]} | {s['url']}"
            for s in top_signals
        )
        prompt = _REDDIT_PROMPT.format(categories=cats, signals=signals_text)
    else:
        signals_text = "\n".join(
            f"{s['keyword']} (rising {s['trend_pct']}%)"
            for s in signals
        )
        prompt = _GOOGLE_PROMPT.format(categories=cats, signals=signals_text)

    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = message.content[0].text.strip()
        # Strip markdown code fences
        if "```" in raw:
            raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
        # Extract JSON array even from partial responses
        match = re.search(r"\[.*\]", raw, re.DOTALL)
        if match:
            raw = match.group(0)
        products = json.loads(raw)
        result = products if isinstance(products, list) else []
        print(f"  LLM extraiu {len(result)} oportunidade(s) de {source}")
        return result
    except Exception as e:
        print(f"  Erro LLM ({source}): {e}")
        return []
