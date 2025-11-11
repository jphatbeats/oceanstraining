"""
FAST DATASET BUILDER - PATH A
Samples 10,000 narratives for quick training start
Uses existing labels from narratives
"""

import json
import random
from pathlib import Path
from tqdm import tqdm

print("=" * 70)
print("FAST DATASET BUILDER - PATH A")
print("=" * 70)

# Paths
NARRATIVES_DIR = Path("N:/OCEANS/narratives")
OUTPUT_DIR = Path("N:/OCEANS/oceans_training/datasets/ocean_intelligence_corpus")
OUTPUT_FILE = OUTPUT_DIR / "training_corpus.jsonl"

# Sample size
SAMPLE_SIZE = 10000

print(f"\nTarget: {SAMPLE_SIZE} samples for training")

# Find all JSON files
print("\nFinding narrative files...")
all_files = list(NARRATIVES_DIR.rglob("*.json"))
print(f"Found {len(all_files)} total files")

# Sample random files
print(f"\nSampling {SAMPLE_SIZE} files...")
sampled_files = random.sample(all_files, min(SAMPLE_SIZE, len(all_files)))

# Process sampled files
print(f"\nProcessing sampled files...")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

corpus = []
for json_file in tqdm(sampled_files, desc="Processing"):
    try:
        if json_file.stat().st_size > 10:  # Skip tiny files
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # Extract text
                if isinstance(data, dict):
                    text = ""

                    # Try different fields
                    if "symbol" in data:
                        text += f"Symbol: {data['symbol']}\n"
                    if "narrative" in data:
                        text += data["narrative"]
                    elif "title" in data:
                        text += data["title"]
                    elif "summary" in data:
                        text += data["summary"]

                    if len(text) > 50:  # Min length
                        # Determine domain from data
                        domain = "social"  # default
                        if "sentiment" in data or "sage_summary" in data:
                            domain = "news"
                        elif "social_score" in data or "galaxy_score" in data:
                            domain = "lunarcrush"

                        corpus.append({
                            "text": text[:512],  # Truncate for efficiency
                            "domain": domain
                        })
    except Exception as e:
        continue

# Save
print(f"\nSaving {len(corpus)} samples...")
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    for item in corpus:
        f.write(json.dumps(item) + '\n')

# Stats
from collections import Counter
domains = Counter(item["domain"] for item in corpus)

print("\n" + "=" * 70)
print(f"CORPUS READY: {len(corpus)} samples")
print(f"Output: {OUTPUT_FILE}")
print("\nDomain distribution:")
for domain, count in domains.items():
    pct = (count / len(corpus)) * 100
    print(f"  {domain}: {count} ({pct:.1f}%)")
print("=" * 70)
