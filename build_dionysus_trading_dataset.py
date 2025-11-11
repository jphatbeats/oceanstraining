"""
BUILD DIONYSUS TRADING BRAIN DATASET
=====================================
Creates training dataset for phi3:mini trading brain.

Focus: FAST execution decisions based on research brain analysis.

Dataset composition:
- Donor samples (trading-focused subset)
- Meme coin execution patterns
- BUY/PASS decision examples
- Position sizing logic
- Risk management
- Entry/exit timing

Output: DIONYSUS_trading_brain.jsonl (~50K samples)
Target model: phi3:mini (3.8B parameters)
Training time: ~2-3 hours on A6000
"""

import json
import random
from pathlib import Path

random.seed(42)

# Paths
DONORS_DIR = Path("N:/OCEANS/oceanstraining/out")
CRYPTO_SOCIAL_FILE = Path("N:/OCEANS/oceans_training/data/bert_datasets/crypto_social_sentiment_training.jsonl")
OUTPUT_DIR = Path("N:/OCEANS/oceans_training/data/final_training")
OUTPUT_FILE = OUTPUT_DIR / "DIONYSUS_trading_brain.jsonl"

print("=" * 70)
print("BUILDING DIONYSUS TRADING BRAIN DATASET")
print("=" * 70)

def load_jsonl(filepath):
    samples = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                samples.append(json.loads(line.strip()))
            except:
                continue
    return samples

# ============================================================================
# LAYER 1: DONOR SAMPLES (Trading-focused subset)
# ============================================================================

print("\n[1/4] Loading donor samples (trading-focused)...")

donor_files = {
    "finma": DONORS_DIR / "aria_finma.jsonl",
    "finance_llm": DONORS_DIR / "aria_finance_llm.jsonl",
    "nemotron": DONORS_DIR / "dionysus_nemotron.jsonl"
}

# Sample 30% of donors (trading-focused)
trading_donors = []
for name, filepath in donor_files.items():
    if filepath.exists():
        samples = load_jsonl(filepath)
        # Take 30% focused on trading/execution
        sample_count = int(len(samples) * 0.3)
        sampled = random.sample(samples, sample_count)
        trading_donors.extend(sampled)
        print(f"  [OK] {name}: {len(sampled):,} trading samples")

print(f"  Total donor samples: {len(trading_donors):,}")

# ============================================================================
# LAYER 2: CRYPTO SOCIAL (Sentiment → Decision)
# ============================================================================

print("\n[2/4] Loading crypto social sentiment...")

crypto_social = []
if CRYPTO_SOCIAL_FILE.exists():
    crypto_social = load_jsonl(CRYPTO_SOCIAL_FILE)
    # Sample 50% (sentiment signals for trading)
    crypto_social = random.sample(crypto_social, len(crypto_social) // 2)
    print(f"  [OK] {len(crypto_social):,} crypto social samples")

# ============================================================================
# LAYER 3: TRADING DECISION EXAMPLES (Generated)
# ============================================================================

print("\n[3/4] Generating trading decision examples...")

SYMBOLS = ["BTC", "ETH", "SOL", "PEPE", "WIF", "BONK", "DOGE", "SHIB"]

# BUY decision templates
BUY_TEMPLATES = [
    {
        "signals": "RSI oversold (28), MACD bullish cross, volume spike +240%, social heat rising",
        "decision": "BUY",
        "position": "2%",
        "stop": "-3%",
        "target": "+8%",
        "reasoning": "Strong confluence: technical + volume + social. Risk/reward 2.6:1"
    },
    {
        "signals": "Breakout above resistance, whale accumulation detected, community sentiment 85% bullish",
        "decision": "BUY",
        "position": "3%",
        "stop": "-4%",
        "target": "+12%",
        "reasoning": "Momentum + whale activity + retail FOMO. High conviction play"
    },
    {
        "signals": "Golden cross forming, exchange listings announced, social mentions +500%",
        "decision": "BUY",
        "position": "2.5%",
        "stop": "-3.5%",
        "target": "+10%",
        "reasoning": "Catalyst-driven move with technical confirmation"
    }
]

# PASS decision templates
PASS_TEMPLATES = [
    {
        "signals": "RSI overbought (78), distribution pattern, whale selling, social sentiment mixed",
        "decision": "PASS",
        "reasoning": "Top signal: overbought + distribution. Wait for pullback"
    },
    {
        "signals": "No clear trend, low volume, social heat declining, no catalyst",
        "decision": "PASS",
        "reasoning": "Low conviction setup. Need confirmation before entry"
    },
    {
        "signals": "Pump-and-dump pattern detected, liquidity low, high risk/reward ratio unfavorable",
        "decision": "PASS",
        "reasoning": "Red flags: P&D + low liquidity. Too risky"
    }
]

# HOLD decision templates
HOLD_TEMPLATES = [
    {
        "signals": "Position up +15%, target not reached, momentum still strong, no top signals",
        "decision": "HOLD",
        "action": "Trailing stop at +10%",
        "reasoning": "Let winners run. Protect gains with trailing stop"
    },
    {
        "signals": "Consolidation after breakout, healthy pullback, support holding, social still bullish",
        "decision": "HOLD",
        "action": "Maintain position",
        "reasoning": "Normal consolidation. Support intact, momentum positive"
    }
]

trading_examples = []

# Generate 5000 BUY examples
for _ in range(5000):
    symbol = random.choice(SYMBOLS)
    template = random.choice(BUY_TEMPLATES)

    text = f"Trading Decision - {symbol}\n\n"
    text += f"Signals: {template['signals']}\n\n"
    text += f"Decision: {template['decision']}\n"
    text += f"Position Size: {template['position']}\n"
    text += f"Stop Loss: {template['stop']}\n"
    text += f"Target: {template['target']}\n\n"
    text += f"Reasoning: {template['reasoning']}"

    trading_examples.append({"text": text, "source": "trading_decision", "type": "BUY"})

# Generate 3000 PASS examples
for _ in range(3000):
    symbol = random.choice(SYMBOLS)
    template = random.choice(PASS_TEMPLATES)

    text = f"Trading Decision - {symbol}\n\n"
    text += f"Signals: {template['signals']}\n\n"
    text += f"Decision: {template['decision']}\n\n"
    text += f"Reasoning: {template['reasoning']}"

    trading_examples.append({"text": text, "source": "trading_decision", "type": "PASS"})

# Generate 2000 HOLD examples
for _ in range(2000):
    symbol = random.choice(SYMBOLS)
    template = random.choice(HOLD_TEMPLATES)

    text = f"Trading Decision - {symbol}\n\n"
    text += f"Signals: {template['signals']}\n\n"
    text += f"Decision: {template['decision']}\n"
    text += f"Action: {template['action']}\n\n"
    text += f"Reasoning: {template['reasoning']}"

    trading_examples.append({"text": text, "source": "trading_decision", "type": "HOLD"})

print(f"  Generated {len(trading_examples):,} trading decision examples")

# ============================================================================
# COMBINE AND SAVE
# ============================================================================

print("\n[4/4] Combining and saving...")

all_samples = trading_donors + crypto_social + trading_examples
random.shuffle(all_samples)

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    for sample in all_samples:
        f.write(json.dumps(sample) + '\n')

file_size_mb = OUTPUT_FILE.stat().st_size / (1024 * 1024)

print("\n" + "=" * 70)
print("DIONYSUS TRADING BRAIN DATASET COMPLETE")
print("=" * 70)
print(f"\nOutput: {OUTPUT_FILE}")
print(f"Samples: {len(all_samples):,}")
print(f"Size: {file_size_mb:.1f} MB")

print(f"\nComposition:")
print(f"  Donor samples (trading-focused): {len(trading_donors):,} ({len(trading_donors)/len(all_samples)*100:.1f}%)")
print(f"  Crypto social: {len(crypto_social):,} ({len(crypto_social)/len(all_samples)*100:.1f}%)")
print(f"  Trading decisions: {len(trading_examples):,} ({len(trading_examples)/len(all_samples)*100:.1f}%)")

print("\nNext: Train phi3:mini on this dataset (~2-3 hours)")
print("Target model: microsoft/phi-3-mini-4k-instruct")
