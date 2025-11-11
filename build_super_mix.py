"""
SUPER-MIX BUILDER - Combines All 5 Data Sources
================================================
Builds complete training corpus with correct ratios:
- Domain + Narratives + Tools: 70% (from existing Halloween corpus)
- Oceans Base (soul): 20% (identity/duties/protocols/relationships)
- Role Episodes: 10% (positive/negative scenarios)

Total target: 158,400 samples per entity (9900 steps × batch 4 × grad_accum 4)

This is THE SUPER-BASE. The moment Oceana becomes ALIVE.
"""

import json
import random
import sys
from pathlib import Path
from typing import List, Dict

# ============================================================================
# CONFIGURATION
# ============================================================================

ENTITY_CONFIGS = {
    "ARIA": {
        "existing_corpus": "N:/OCEANS/oceans_training/datasets/ocean_intelligence_corpus/training_corpus.jsonl",
        "description": "Intelligence Coordinator with Ocean Scanner, Trident, TAAPI API knowledge"
    },
    "DIONYSUS": {
        "existing_corpus": "N:/OCEANS/oceans_training/datasets/dionysus_meme_intelligence/training_corpus_final.jsonl",
        "description": "Meme God with LunarCrush, GoPlus, DexScreener API knowledge"
    },
    "HYDRA": {
        "existing_corpus": "N:/OCEANS/oceans_training/datasets/ocean_intelligence_corpus/training_corpus.jsonl",
        "description": "Social Oracle with LunarCrush social intelligence (shares corpus with ARIA/SAGE)"
    },
    "SAGE": {
        "existing_corpus": "N:/OCEANS/oceans_training/datasets/ocean_intelligence_corpus/training_corpus.jsonl",
        "description": "News Oracle with RSS feed processing (shares corpus with ARIA/HYDRA)"
    }
}

# Target samples
TOTAL_TARGET = 158400  # 9900 steps × 16 effective batch
DOMAIN_TARGET = int(TOTAL_TARGET * 0.60)      # 95,040 from existing corpus
SOUL_TARGET = int(TOTAL_TARGET * 0.20)        # 31,680 from Oceans Base
ROLES_TARGET = int(TOTAL_TARGET * 0.10)       # 15,840 from role episodes
SPECIALIZED_TARGET = int(TOTAL_TARGET * 0.10) # 15,840 from specialized knowledge

# Paths
OCEANS_BASE_DIR = Path("N:/OCEANS/oceans_training/data/oceans_base")
ROLE_EPISODES_DIR = Path("N:/OCEANS/oceans_training/data/role_episodes")
SPECIALIZED_DIR = Path("N:/OCEANS/oceans_training/data/specialized_knowledge")
OUTPUT_DIR = Path("N:/OCEANS/oceans_training/data/super_mix")

# ============================================================================
# DATA LOADING
# ============================================================================

def load_jsonl(path: Path) -> List[Dict]:
    """Load JSONL file"""
    samples = []
    if not path.exists():
        print(f"[!] WARNING: {path} does not exist")
        return samples

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                samples.append(json.loads(line))
            except:
                pass
    return samples

def load_oceans_base() -> List[Dict]:
    """Load all Oceans Base cards (identity, duties, protocols, tools, relationships, etiquette)"""
    all_cards = []

    card_files = [
        "identity_cards.jsonl",
        "duties_cards.jsonl",
        "protocol_cards.jsonl",
        "tool_cards.jsonl",
        "relationship_cards.jsonl",
        "etiquette_cards.jsonl"
    ]

    for filename in card_files:
        filepath = OCEANS_BASE_DIR / filename
        cards = load_jsonl(filepath)
        all_cards.extend(cards)
        print(f"  Loaded {len(cards)} cards from {filename}")

    return all_cards

def load_role_episodes(entity_name: str) -> List[Dict]:
    """Load role episodes for specific entity"""
    filepath = ROLE_EPISODES_DIR / f"{entity_name}_episodes.jsonl"
    episodes = load_jsonl(filepath)
    print(f"  Loaded {len(episodes)} role episodes for {entity_name}")
    return episodes

def load_existing_corpus(corpus_path: str) -> List[Dict]:
    """Load existing training corpus (domain + API training from Halloween)"""
    samples = load_jsonl(Path(corpus_path))
    print(f"  Loaded {len(samples)} samples from existing corpus")
    return samples

def load_specialized_knowledge() -> List[Dict]:
    """Load specialized knowledge layer (FinGPT, FinBERT, CryptoBERT, etc.)"""
    filepath = SPECIALIZED_DIR / "specialized_knowledge.jsonl"
    knowledge = load_jsonl(filepath)
    print(f"  Loaded {len(knowledge)} specialized knowledge examples")
    return knowledge

# ============================================================================
# SAMPLING & EXPANSION
# ============================================================================

def sample_with_replacement(items: List[Dict], target_count: int) -> List[Dict]:
    """Sample items with replacement to reach target count"""
    if len(items) >= target_count:
        return random.sample(items, target_count)
    else:
        # Need to sample with replacement
        return random.choices(items, k=target_count)

def expand_episodes(episodes: List[Dict], target_count: int) -> List[Dict]:
    """Expand role episodes through paraphrasing and repetition"""
    if not episodes:
        return []

    expanded = []

    # Repeat episodes to reach target
    repeats_needed = (target_count // len(episodes)) + 1

    for _ in range(repeats_needed):
        for episode in episodes:
            if len(expanded) >= target_count:
                break
            expanded.append(episode)
        if len(expanded) >= target_count:
            break

    return expanded[:target_count]

# ============================================================================
# CORPUS BUILDING
# ============================================================================

def build_super_mix(entity_name: str) -> Dict:
    """Build complete super-mix corpus for entity"""

    print(f"\n{'=' * 70}")
    print(f"BUILDING SUPER-MIX FOR {entity_name}")
    print(f"{'=' * 70}")

    config = ENTITY_CONFIGS[entity_name]

    # 1. Load all sources
    print(f"\n[1/6] Loading data sources...")
    existing_corpus = load_existing_corpus(config["existing_corpus"])
    oceans_base = load_oceans_base()
    role_episodes = load_role_episodes(entity_name)
    specialized_knowledge = load_specialized_knowledge()

    print(f"\n  Source sizes:")
    print(f"    Existing corpus: {len(existing_corpus):,}")
    print(f"    Oceans Base cards: {len(oceans_base)}")
    print(f"    Role episodes: {len(role_episodes)}")
    print(f"    Specialized knowledge: {len(specialized_knowledge)}")

    # 2. Sample/expand to targets
    print(f"\n[2/6] Sampling to target counts...")
    print(f"    Domain+Narratives+Tools (60%): {DOMAIN_TARGET:,} samples")
    print(f"    Oceans Base (20%): {SOUL_TARGET:,} samples")
    print(f"    Role Episodes (10%): {ROLES_TARGET:,} samples")
    print(f"    Specialized Knowledge (10%): {SPECIALIZED_TARGET:,} samples")

    # Sample existing corpus (domain + narratives + tools combined)
    domain_samples = random.sample(existing_corpus, min(DOMAIN_TARGET, len(existing_corpus)))
    if len(domain_samples) < DOMAIN_TARGET:
        print(f"    [!] Corpus only has {len(existing_corpus):,}, sampling with replacement")
        domain_samples = sample_with_replacement(existing_corpus, DOMAIN_TARGET)

    # Repeat Oceans Base cards 100x then sample
    oceans_base_repeated = oceans_base * 100
    print(f"    Oceans Base repeated 100x: {len(oceans_base_repeated):,} total cards")
    soul_samples = sample_with_replacement(oceans_base_repeated, SOUL_TARGET)

    # Expand role episodes
    role_samples = expand_episodes(role_episodes, ROLES_TARGET)

    # Repeat specialized knowledge to reach target
    specialized_repeated = specialized_knowledge * ((SPECIALIZED_TARGET // len(specialized_knowledge)) + 1)
    specialized_samples = sample_with_replacement(specialized_repeated, SPECIALIZED_TARGET)

    print(f"\n  Sampled counts:")
    print(f"    Domain: {len(domain_samples):,}")
    print(f"    Soul: {len(soul_samples):,}")
    print(f"    Roles: {len(role_samples):,}")
    print(f"    Specialized: {len(specialized_samples):,}")
    print(f"    Total: {len(domain_samples) + len(soul_samples) + len(role_samples) + len(specialized_samples):,}")

    # 3. Combine and shuffle
    print(f"\n[3/6] Combining and shuffling...")
    all_samples = domain_samples + soul_samples + role_samples + specialized_samples
    random.shuffle(all_samples)

    # 4. Convert to training format
    print(f"\n[4/6] Converting to training format...")
    training_samples = []
    for i, sample in enumerate(all_samples):
        # Extract text field (handle different source formats)
        if "text" in sample:
            text = sample["text"]
        elif "content" in sample:
            text = sample["content"]
        else:
            text = str(sample)

        # Create training sample
        training_sample = {"text": text}
        training_samples.append(training_sample)

        if (i + 1) % 10000 == 0:
            print(f"    Processed {i + 1:,} / {len(all_samples):,} samples")

    # 5. Save
    print(f"\n[6/6] Saving super-mix corpus...")
    output_path = OUTPUT_DIR / f"{entity_name}_super_mix.jsonl"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        for sample in training_samples:
            f.write(json.dumps(sample) + '\n')

    file_size_mb = output_path.stat().st_size / (1024 * 1024)

    print(f"\n{'=' * 70}")
    print(f"{entity_name} SUPER-MIX COMPLETE")
    print(f"{'=' * 70}")
    print(f"Output: {output_path}")
    print(f"Size: {file_size_mb:.1f} MB")
    print(f"Samples: {len(training_samples):,}")
    print(f"\nMix breakdown:")
    print(f"  - Domain+Narratives+Tools: {len(domain_samples):,} ({len(domain_samples)/len(training_samples)*100:.1f}%)")
    print(f"  - Oceans Base (soul): {len(soul_samples):,} ({len(soul_samples)/len(training_samples)*100:.1f}%)")
    print(f"  - Role Episodes: {len(role_samples):,} ({len(role_samples)/len(training_samples)*100:.1f}%)")
    print(f"  - Specialized Knowledge: {len(specialized_samples):,} ({len(specialized_samples)/len(training_samples)*100:.1f}%)")
    print(f"{'=' * 70}\n")

    return {
        "entity": entity_name,
        "output_path": str(output_path),
        "total_samples": len(training_samples),
        "file_size_mb": file_size_mb,
        "mix": {
            "domain": len(domain_samples),
            "soul": len(soul_samples),
            "roles": len(role_samples)
        }
    }

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Build super-mix for all entities"""

    print("=" * 70)
    print("SUPER-MIX BUILDER - THE BIRTH OF OCEANA")
    print("=" * 70)
    print()
    print("Building complete training corpora with soul + domain + roles")
    print()
    print(f"Target: {TOTAL_TARGET:,} samples per entity")
    print(f"  - Domain+Narratives+Tools: 70% ({DOMAIN_TARGET:,})")
    print(f"  - Oceans Base (soul): 20% ({SOUL_TARGET:,})")
    print(f"  - Role Episodes: 10% ({ROLES_TARGET:,})")
    print()
    print("=" * 70)

    # Set random seed for reproducibility
    random.seed(42)

    # Build for each entity
    results = []
    entities = ["ARIA", "SAGE", "HYDRA", "DIONYSUS"]

    for entity in entities:
        try:
            result = build_super_mix(entity)
            results.append(result)
        except Exception as e:
            print(f"\n[ERROR] Failed to build {entity}: {e}")
            import traceback
            traceback.print_exc()

    # Summary
    print("\n" + "=" * 70)
    print("SUPER-MIX GENERATION COMPLETE")
    print("=" * 70)
    print(f"\nGenerated {len(results)} super-mix corpora:")
    for result in results:
        print(f"  {result['entity']}: {result['total_samples']:,} samples ({result['file_size_mb']:.1f} MB)")

    print(f"\nTotal corpus size: {sum(r['file_size_mb'] for r in results):.1f} MB")
    print(f"Total samples: {sum(r['total_samples'] for r in results):,}")

    print()
    print("These corpora contain:")
    print("  1. WHO they are (identity)")
    print("  2. WHAT they do (duties)")
    print("  3. HOW they communicate (protocols)")
    print("  4. WHAT tools they have (APIs)")
    print("  5. WHO their partners are (relationships)")
    print("  6. WHAT to do (positive role episodes)")
    print("  7. WHAT NOT to do (negative role episodes)")
    print("  8. Domain expertise (crypto/meme/social/news)")
    print("  9. API usage patterns (Ocean Scanner, LunarCrush, GoPlus, etc.)")
    print()
    print("Next step: Update training scripts to use super-mix corpus")
    print("Then: TRAIN! (~6.9 hours per entity, ~27.6 hours total)")
    print("=" * 70)

if __name__ == "__main__":
    main()
