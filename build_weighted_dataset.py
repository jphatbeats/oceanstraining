"""
OCEAN WEIGHTED DATASET BUILDER
Builds unified corpus with domain weighting:
- News (SAGE): 35%
- Social (HYDRA): 30%
- LunarCrush (HYDRA): 25%
- Community (HYDRA): 10%
"""

import json
import random
from pathlib import Path
from typing import List, Dict
from tqdm import tqdm

print("=" * 70)
print("OCEAN WEIGHTED DATASET BUILDER")
print("=" * 70)

# Paths
NARRATIVES_DIR = Path("N:/OCEANS/narratives")
NEWS_DIR = Path("N:/OCEANS/news_scanners")
LUNAR_DIR = Path("N:/OCEANS/lunarcrush_scanners")
OUTPUT_DIR = Path("N:/OCEANS/oceans_training/datasets/ocean_intelligence_corpus")

# Domain weights (must sum to 1.0)
WEIGHTS = {
    "news": 0.35,      # SAGE domain
    "social": 0.30,    # HYDRA domain
    "lunarcrush": 0.25,  # HYDRA domain
    "community": 0.10   # HYDRA domain
}

def load_narratives() -> List[Dict]:
    """Load all 34,902 narrative files"""
    print("\n[1/4] Loading narratives...")
    narratives = []

    for json_file in tqdm(list(NARRATIVES_DIR.rglob("*.json")), desc="Narratives"):
        try:
            if json_file.stat().st_size > 10:  # Skip tiny files
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        narratives.append({
                            "source": "narrative",
                            "data": data,
                            "file": str(json_file)
                        })
        except Exception as e:
            continue

    print(f"  ✅ Loaded {len(narratives)} narratives")
    return narratives

def load_news() -> List[Dict]:
    """Load news/RSS articles"""
    print("\n[2/4] Loading news articles...")
    news = []

    # Global news feed
    global_news_path = Path("N:/OCEANS/narratives/global_news_feed.json")
    if global_news_path.exists():
        with open(global_news_path, 'r', encoding='utf-8') as f:
            feed = json.load(f)
            for article in feed:
                news.append({
                    "source": "news",
                    "data": article
                })

    # RSS articles
    rss_path = NEWS_DIR / "news_scanners" / "data" / "headlines" / "latest_rss_articles.json"
    if rss_path.exists():
        with open(rss_path, 'r', encoding='utf-8') as f:
            articles = json.load(f)
            for article in articles:
                news.append({
                    "source": "news",
                    "data": article
                })

    print(f"  ✅ Loaded {len(news)} news articles")
    return news

def load_lunarcrush() -> List[Dict]:
    """Load LunarCrush social data"""
    print("\n[3/4] Loading LunarCrush data...")
    lunar = []

    # Raw galaxy data
    galaxy_path = LUNAR_DIR / "raw_galaxy_data_20250905_171936.json"
    if galaxy_path.exists():
        with open(galaxy_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    lunar.append({
                        "source": "lunarcrush",
                        "data": item
                    })
            elif isinstance(data, dict) and "data" in data:
                for item in data["data"]:
                    lunar.append({
                        "source": "lunarcrush",
                        "data": item
                    })

    # AI analysis results
    for result_file in LUNAR_DIR.glob("ai_analysis_results_*.json"):
        try:
            with open(result_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                lunar.append({
                    "source": "lunarcrush",
                    "data": data
                })
        except:
            continue

    print(f"  ✅ Loaded {len(lunar)} LunarCrush samples")
    return lunar

def extract_text(item: Dict) -> str:
    """Extract text content from various data formats"""
    data = item.get("data", {})
    source = item.get("source", "")

    # News/RSS
    if source == "news":
        title = data.get("title", "")
        summary = data.get("summary", "") or data.get("sage_summary", "")
        return f"{title}\n{summary}"

    # LunarCrush
    elif source == "lunarcrush":
        text_parts = []
        if "name" in data:
            text_parts.append(f"Token: {data['name']}")
        if "social_score" in data:
            text_parts.append(f"Social Score: {data['social_score']}")
        if "galaxy_score" in data:
            text_parts.append(f"Galaxy Score: {data['galaxy_score']}")
        return "\n".join(text_parts)

    # Narratives
    elif source == "narrative":
        text_parts = []
        if "symbol" in data:
            text_parts.append(f"Symbol: {data['symbol']}")
        if "narrative" in data:
            text_parts.append(data["narrative"])
        return "\n".join(text_parts)

    # Fallback
    return str(data)[:500]

def build_corpus(narratives: List[Dict], news: List[Dict], lunar: List[Dict]) -> List[Dict]:
    """Build weighted corpus"""
    print("\n[4/4] Building weighted corpus...")

    # Calculate target counts based on smallest domain
    total_items = min(len(news), len(lunar), len(narratives))
    target_counts = {
        "news": int(total_items * WEIGHTS["news"] / min(WEIGHTS.values())),
        "social": int(total_items * WEIGHTS["social"] / min(WEIGHTS.values())),
        "lunarcrush": int(total_items * WEIGHTS["lunarcrush"] / min(WEIGHTS.values())),
        "community": int(total_items * WEIGHTS["community"] / min(WEIGHTS.values()))
    }

    print(f"\n  Target sample counts:")
    for domain, count in target_counts.items():
        print(f"    {domain}: {count} samples ({WEIGHTS[domain]*100:.0f}%)")

    corpus = []

    # Add news (35%)
    sampled_news = random.sample(news, min(len(news), target_counts["news"]))
    for item in sampled_news:
        text = extract_text(item)
        if len(text) > 50:  # Min length filter
            corpus.append({
                "domain": "news",
                "text": text,
                "metadata": item["data"]
            })

    # Add social from narratives (30%)
    social_narratives = random.sample(narratives, min(len(narratives), target_counts["social"]))
    for item in social_narratives:
        text = extract_text(item)
        if len(text) > 50:
            corpus.append({
                "domain": "social",
                "text": text,
                "metadata": item["data"]
            })

    # Add LunarCrush (25%)
    sampled_lunar = random.sample(lunar, min(len(lunar), target_counts["lunarcrush"]))
    for item in sampled_lunar:
        text = extract_text(item)
        if len(text) > 50:
            corpus.append({
                "domain": "lunarcrush",
                "text": text,
                "metadata": item["data"]
            })

    # Add community from remaining narratives (10%)
    remaining_narratives = [n for n in narratives if n not in social_narratives]
    community_samples = random.sample(remaining_narratives, min(len(remaining_narratives), target_counts["community"]))
    for item in community_samples:
        text = extract_text(item)
        if len(text) > 50:
            corpus.append({
                "domain": "community",
                "text": text,
                "metadata": item["data"]
            })

    # Shuffle
    random.shuffle(corpus)

    print(f"\n  ✅ Built corpus with {len(corpus)} total samples")
    print(f"\n  Final distribution:")
    from collections import Counter
    domain_counts = Counter(item["domain"] for item in corpus)
    for domain, count in domain_counts.items():
        pct = (count / len(corpus)) * 100
        print(f"    {domain}: {count} ({pct:.1f}%)")

    return corpus

def main():
    # Load all data
    narratives = load_narratives()
    news = load_news()
    lunar = load_lunarcrush()

    # Build corpus
    corpus = build_corpus(narratives, news, lunar)

    # Save
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "raw_corpus.jsonl"

    print(f"\nSaving to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in corpus:
            f.write(json.dumps(item) + '\n')

    print("\n" + "=" * 70)
    print(f"✅ CORPUS READY: {len(corpus)} samples")
    print(f"   Output: {output_path}")
    print("=" * 70)

if __name__ == "__main__":
    random.seed(42)  # Reproducibility
    main()
