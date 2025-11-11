"""
SPECIALIZED KNOWLEDGE LAYER GENERATOR
======================================
Generates synthetic training examples INSPIRED BY specialized models.
These examples teach the STYLE of analysis these models would do.

Output: specialized_knowledge.jsonl in data/specialized_knowledge/
"""

import json
import random
from pathlib import Path
from typing import List, Dict

OUTPUT_DIR = Path("N:/OCEANS/oceans_training/data/specialized_knowledge")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Crypto symbols for examples
SYMBOLS = ["BTC", "ETH", "SOL", "AVAX", "MATIC", "LINK", "UNI", "AAVE", "PEPE", "SHIB", "DOGE", "WIF"]

# ============================================================================
# FINGPT-STYLE: Financial Analysis & Forecasting
# ============================================================================

def generate_fingpt_examples() -> List[Dict]:
    """FinGPT-style financial analysis and forecasting examples"""
    examples = []

    templates = [
        {
            "input": "Analyze the technical setup for {symbol} and provide a 24-hour price forecast.",
            "output": "Technical Analysis for {symbol}:\n\nCurrent Price: ${price}\nRSI(14): {rsi} - {rsi_signal}\nMACD: {macd_signal}\nBollinger Position: {bb_position}\n\n24h Forecast: {forecast}\nConfidence: {confidence}%\nKey Levels: Support ${support}, Resistance ${resistance}\n\nRationale: {rationale}"
        },
        {
            "input": "What is the market structure for {symbol} on the 4H timeframe?",
            "output": "Market Structure Analysis ({symbol} 4H):\n\nTrend: {trend}\nStructure: {structure}\nKey Pivot: ${pivot}\n\nBias: {bias}\nInvalidation: {invalidation}\n\nThe {structure} structure suggests {implication}."
        }
    ]

    for _ in range(30):
        symbol = random.choice(SYMBOLS)
        template = random.choice(templates)

        price = random.randint(100, 90000)
        rsi = random.randint(30, 70)
        rsi_signal = "Oversold" if rsi < 35 else "Neutral" if rsi < 65 else "Overbought"

        text = template["input"].format(symbol=symbol)
        text += "\n\n" + template["output"].format(
            symbol=symbol,
            price=price,
            rsi=rsi,
            rsi_signal=rsi_signal,
            macd_signal=random.choice(["Bullish crossover", "Bearish crossover", "Consolidating"]),
            bb_position=random.choice(["Upper band", "Middle band", "Lower band"]),
            forecast=random.choice(["Bullish continuation", "Bearish reversal", "Range-bound"]),
            confidence=random.randint(65, 85),
            support=price - random.randint(100, 500),
            resistance=price + random.randint(100, 500),
            rationale=random.choice([
                "Strong momentum with volume confirmation",
                "Divergence suggests potential reversal",
                "Consolidation near key resistance level"
            ]),
            trend=random.choice(["Uptrend", "Downtrend", "Sideways"]),
            structure=random.choice(["Higher highs/higher lows", "Lower highs/lower lows", "Range-bound"]),
            pivot=price,
            bias=random.choice(["Bullish", "Bearish", "Neutral"]),
            invalidation=random.choice(["Break below $X", "Break above $Y", "Loss of structure"]),
            implication=random.choice([
                "continuation is likely with volume confirmation",
                "reversal is possible if key level breaks",
                "patience is required for directional clarity"
            ])
        )

        examples.append({"text": text, "type": "fingpt_analysis"})

    return examples


# ============================================================================
# FINBERT-STYLE: Sentiment Classification
# ============================================================================

def generate_finbert_examples() -> List[Dict]:
    """FinBERT-style sentiment classification examples"""
    examples = []

    news_items = [
        ("Bitcoin ETF approval rumors intensify as SEC delays decision", "positive", 0.72),
        ("Ethereum network congestion causes gas fees to spike", "negative", 0.65),
        ("Major crypto exchange announces proof-of-reserves audit", "positive", 0.68),
        ("Regulatory uncertainty clouds crypto market outlook", "negative", 0.71),
        ("Institutional adoption of digital assets accelerates", "positive", 0.79),
        ("DeFi protocol suffers smart contract exploit", "negative", 0.82),
        ("Layer 2 scaling solutions show promising transaction throughput", "positive", 0.66),
        ("Crypto lending platform pauses withdrawals amid liquidity concerns", "negative", 0.88),
    ]

    for headline, sentiment, score in news_items * 4:  # Repeat 4x
        text = f"Classify sentiment: \"{headline}\"\n\n"
        text += f"Sentiment: {sentiment.upper()}\n"
        text += f"Confidence: {score:.2f}\n"
        text += f"Impact: {random.choice(['High', 'Medium', 'Low'])}\n\n"
        text += f"Analysis: The headline conveys {sentiment} sentiment due to {random.choice(['regulatory implications', 'technical developments', 'market dynamics', 'institutional activity'])}."

        examples.append({"text": text, "type": "finbert_sentiment"})

    return examples


# ============================================================================
# CRYPTOBERT-STYLE: On-Chain & Tokenomics Analysis
# ============================================================================

def generate_cryptobert_examples() -> List[Dict]:
    """CryptoBERT-style on-chain and tokenomics analysis"""
    examples = []

    templates = [
        {
            "input": "Analyze the tokenomics for {symbol}",
            "output": "Tokenomics Analysis: {symbol}\n\nSupply Metrics:\n- Circulating: {circ}M\n- Total: {total}M\n- Max: {max_supply}\n- Inflation Rate: {inflation}%\n\nDistribution:\n- Top 10 holders: {top10}%\n- Exchange holdings: {exchange}%\n- Burn mechanism: {burn}\n\nAssessment: {assessment}"
        },
        {
            "input": "What does on-chain data show for {symbol}?",
            "output": "On-Chain Analysis: {symbol}\n\nActivity:\n- Active addresses (24h): {addresses}\n- Transaction volume: ${volume}M\n- Exchange inflows: {inflow} (${inflow_usd}M)\n- Exchange outflows: {outflow} (${outflow_usd}M)\n\nSignal: {signal}\n\nInterpretation: {interpretation}"
        }
    ]

    for _ in range(25):
        symbol = random.choice(SYMBOLS)
        template = random.choice(templates)

        text = template["input"].format(symbol=symbol)
        text += "\n\n" + template["output"].format(
            symbol=symbol,
            circ=random.randint(50, 500),
            total=random.randint(100, 1000),
            max_supply=random.choice(["1000M", "Unlimited", "Fixed"]),
            inflation=round(random.uniform(0, 10), 2),
            top10=random.randint(20, 60),
            exchange=random.randint(10, 40),
            burn=random.choice(["Active", "None", "Periodic"]),
            assessment=random.choice([
                "Moderate centralization with deflationary pressure",
                "Healthy distribution with low inflation",
                "High concentration risk, monitor whale movements"
            ]),
            addresses=f"{random.randint(10, 200)}K",
            volume=random.randint(100, 5000),
            inflow=random.choice(["Increasing", "Decreasing", "Stable"]),
            inflow_usd=random.randint(10, 500),
            outflow=random.choice(["Increasing", "Decreasing", "Stable"]),
            outflow_usd=random.randint(10, 500),
            signal=random.choice(["Accumulation phase", "Distribution phase", "Neutral"]),
            interpretation=random.choice([
                "Decreasing exchange supply suggests accumulation by HODLers",
                "Rising exchange inflows may indicate selling pressure",
                "Stable metrics indicate consolidation phase"
            ])
        )

        examples.append({"text": text, "type": "cryptobert_onchain"})

    return examples


# ============================================================================
# ROBERTA-SOCIAL-STYLE: Social Sentiment Analysis
# ============================================================================

def generate_social_sentiment_examples() -> List[Dict]:
    """RoBERTa-style social media sentiment analysis"""
    examples = []

    social_posts = [
        ("Just loaded up on more $BTC, this dip is a gift", "BULLISH", 0.85),
        ("Concerned about $ETH gas fees, this is unsustainable", "BEARISH", 0.72),
        ("$SOL ecosystem is thriving, so many new projects", "BULLISH", 0.79),
        ("Another day, another $DOGE pump and dump", "BEARISH", 0.68),
        ("$AVAX subnet launch is a game changer for scalability", "BULLISH", 0.81),
        ("Regulatory FUD hitting hard, time to take profits", "BEARISH", 0.75),
    ]

    for post, sentiment, score in social_posts * 5:  # Repeat 5x
        text = f"Analyze social sentiment: \"{post}\"\n\n"
        text += f"Sentiment: {sentiment}\n"
        text += f"Confidence: {score:.2f}\n"
        text += f"Toxicity: {random.choice(['Low', 'Medium', 'High'])}\n"
        text += f"Bot likelihood: {random.randint(5, 40)}%\n\n"
        text += f"Context: {random.choice(['Retail sentiment', 'Influencer opinion', 'Community discussion'])}"

        examples.append({"text": text, "type": "social_sentiment"})

    return examples


# ============================================================================
# TOXIC-BERT-STYLE: Scam Detection
# ============================================================================

def generate_scam_detection_examples() -> List[Dict]:
    """ToxicBERT-style scam and spam detection"""
    examples = []

    messages = [
        ("Send 1 ETH to this address and get 10 ETH back!", True, 0.98),
        ("New airdrop claim your free tokens now!", True, 0.85),
        ("BREAKING: Analyzing BTC technical setup", False, 0.12),
        ("Project launched with rug pull protection", False, 0.25),
        ("100x guaranteed join our pump group", True, 0.92),
        ("Whale alert: Large transfer detected", False, 0.08),
    ]

    for msg, is_scam, score in messages * 5:  # Repeat 5x
        text = f"Detect scam: \"{msg}\"\n\n"
        text += f"Classification: {'SCAM' if is_scam else 'LEGITIMATE'}\n"
        text += f"Confidence: {score:.2f}\n"
        text += f"Red flags: {random.choice(['Unrealistic promises', 'Urgency tactics', 'None detected', 'Suspicious links'])}\n\n"
        text += f"Action: {'Block and report' if is_scam else 'Allow'}"

        examples.append({"text": text, "type": "scam_detection"})

    return examples


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Generate all specialized knowledge examples"""

    print("=" * 70)
    print("SPECIALIZED KNOWLEDGE LAYER GENERATOR")
    print("=" * 70)

    all_examples = []

    print("\n[1/5] Generating FinGPT-style examples...")
    fingpt = generate_fingpt_examples()
    all_examples.extend(fingpt)
    print(f"  Generated {len(fingpt)} FinGPT examples")

    print("\n[2/5] Generating FinBERT-style examples...")
    finbert = generate_finbert_examples()
    all_examples.extend(finbert)
    print(f"  Generated {len(finbert)} FinBERT examples")

    print("\n[3/5] Generating CryptoBERT-style examples...")
    cryptobert = generate_cryptobert_examples()
    all_examples.extend(cryptobert)
    print(f"  Generated {len(cryptobert)} CryptoBERT examples")

    print("\n[4/5] Generating Social Sentiment examples...")
    social = generate_social_sentiment_examples()
    all_examples.extend(social)
    print(f"  Generated {len(social)} Social Sentiment examples")

    print("\n[5/5] Generating Scam Detection examples...")
    scam = generate_scam_detection_examples()
    all_examples.extend(scam)
    print(f"  Generated {len(scam)} Scam Detection examples")

    # Shuffle
    random.shuffle(all_examples)

    # Save
    output_file = OUTPUT_DIR / "specialized_knowledge.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in all_examples:
            f.write(json.dumps(example) + '\n')

    print(f"\n{'=' * 70}")
    print(f"SPECIALIZED KNOWLEDGE GENERATION COMPLETE")
    print(f"{'=' * 70}")
    print(f"Output: {output_file}")
    print(f"Total examples: {len(all_examples)}")
    print(f"{'=' * 70}\n")


if __name__ == "__main__":
    main()
