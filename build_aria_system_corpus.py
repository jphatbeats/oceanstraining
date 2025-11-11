"""
ARIA SYSTEM-AWARE TRAINING CORPUS BUILDER
Teaches ARIA how to use Ocean infrastructure:
- Ocean Scanner API (technical analysis)
- Trident backtesting system
- TAAPI indicators interpretation
- Multi-source data fusion
- Event bus messaging
- Cross-AI coordination
"""

import json
from pathlib import Path

print("=" * 70)
print("BUILDING ARIA SYSTEM-AWARE TRAINING CORPUS")
print("=" * 70)

OUTPUT_DIR = Path("N:/OCEANS/oceans_training/datasets/aria_intelligence")
OUTPUT_FILE = OUTPUT_DIR / "training_corpus.jsonl"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

corpus = []

# === SECTION 1: OCEAN SCANNER API USAGE ===
print("\n[1/7] Ocean Scanner API knowledge...")

corpus.append({
    "text": """Task: Get technical analysis for Bitcoin

ARIA Action:
1. Query Ocean Scanner API: GET http://localhost:5000/api/ocean_scanner/BTC
2. Parse response:
   - RSI_14: 45.2 (neutral, not overbought/oversold)
   - MACD: 0.025 (bullish crossover detected)
   - BBANDS_upper: 68500, middle: 65000, lower: 61500 (price near middle band)
   - Volume_24h: 2.8B (increasing, confirms trend)
3. Interpretation: Technical setup is BULLISH with room to run
4. Next: Cross-reference with social sentiment for confluence""",
    "domain": "ocean_scanner_api",
    "task": "technical_analysis"
})

corpus.append({
    "text": """Task: Scan multiple coins for technical breakouts

ARIA Action:
1. Batch query: GET http://localhost:5000/api/ocean_scanner/batch?symbols=BTC,ETH,SOL,AVAX
2. Filter for breakout conditions:
   - RSI > 50 and < 70 (bullish momentum, not overbought)
   - MACD > 0 (positive momentum)
   - Volume > 20% above 24h average
3. Found candidates: ETH (RSI 62, MACD 0.18, Vol +35%)
4. Action: Send event to TRITON for opportunity review""",
    "domain": "ocean_scanner_api",
    "task": "batch_scanning"
})

# === SECTION 2: TRIDENT BACKTESTING ===
print("[2/7] Trident backtesting workflows...")

corpus.append({
    "text": """Task: Validate trading strategy before recommending to TRITON

ARIA Action:
1. Call Trident: POST http://localhost:5001/api/trident/backtest
   Body: {
     "symbol": "BTC",
     "strategies": ["RSI_14_30_70", "MACD_CROSS", "BBANDS_SQUEEZE"],
     "timeframe": "1h",
     "lookback_days": 30
   }
2. Analyze results:
   - RSI_14_30_70: 18.5% return, 68% win rate, Sharpe 1.8 (EXCELLENT)
   - MACD_CROSS: 12.2% return, 55% win rate, Sharpe 1.2 (GOOD)
   - BBANDS_SQUEEZE: -3.1% return, 45% win rate (REJECT)
3. TRITON STAMP: RSI_14_30_70 passes (>60% win rate, >1.5 Sharpe)
4. Recommendation: Use RSI strategy for BTC entry""",
    "domain": "trident_backtesting",
    "task": "strategy_validation"
})

# === SECTION 3: MULTI-SOURCE CONFLUENCE ===
print("[3/7] Multi-source intelligence fusion...")

corpus.append({
    "text": """Task: Detect high-confidence trading opportunity via confluence

ARIA Process:
1. Technical (Ocean Scanner): BTC showing bullish MACD crossover, RSI 52
2. Social (HYDRA via event bus): Galaxy Score 75, sentiment 82% bullish, +45% social volume
3. News (SAGE via event bus): Breaking: Major institution announces BTC allocation
4. Lead Delta Analysis: Social spike 2.3 hours BEFORE price move (predictive signal)
5. Confluence Score: 3/3 sources ALIGNED = HIGH CONFIDENCE
6. Narrative Velocity: Fast (news + social moving together)
7. Action: Generate research package for TRITON with 85% confidence score""",
    "domain": "confluence_detection",
    "task": "multi_source_fusion"
})

corpus.append({
    "text": """Task: Reject low-confidence signal (no confluence)

ARIA Process:
1. Technical: ETH RSI overbought at 78 (warning sign)
2. Social (HYDRA): Galaxy Score 45, sentiment neutral, volume declining
3. News (SAGE): No significant news in 48 hours
4. Confluence Score: 1/3 sources (technical only) = LOW CONFIDENCE
5. Narrative Velocity: Slow (no catalyst)
6. Action: SKIP opportunity, wait for better confluence""",
    "domain": "confluence_detection",
    "task": "signal_rejection"
})

# === SECTION 4: TAAPI INDICATORS ===
print("[4/7] TAAPI indicator interpretation...")

corpus.append({
    "text": """Task: Interpret RSI indicator for trading decision

ARIA Knowledge:
- RSI < 30: Oversold (potential BUY signal if trend reversing)
- RSI 30-50: Bearish momentum (wait for confirmation)
- RSI 50-70: Bullish momentum (ideal entry zone)
- RSI > 70: Overbought (potential SELL signal or take profit)

Current: BTC RSI = 58
Interpretation: Bullish momentum, room to run before overbought
Action: FAVORABLE for entry if other signals confirm""",
    "domain": "taapi_indicators",
    "task": "rsi_interpretation"
})

corpus.append({
    "text": """Task: MACD crossover analysis

ARIA Knowledge:
- MACD crosses above signal line = BULLISH (momentum shift up)
- MACD crosses below signal line = BEARISH (momentum shift down)
- Histogram expanding = strength increasing
- Histogram contracting = strength weakening

Current: ETH MACD crossed above signal 3 hours ago, histogram expanding
Interpretation: Fresh bullish momentum, strong confirmation
Action: STRONG BUY signal if confluence with other sources""",
    "domain": "taapi_indicators",
    "task": "macd_analysis"
})

# === SECTION 5: EVENT BUS COMMUNICATION ===
print("[5/7] Event bus messaging patterns...")

corpus.append({
    "text": """Task: Send opportunity alert to TRITON via event bus

ARIA Action:
1. Publish to channel: ocean:confluence
   Message: {
     "type": "OPPORTUNITY_DETECTED",
     "symbol": "BTC",
     "confidence": 0.85,
     "sources": ["technical", "social", "news"],
     "signals": {
       "technical": {"rsi": 58, "macd": "bullish_cross"},
       "social": {"galaxy_score": 75, "sentiment": 0.82},
       "news": {"headline": "Institution announces BTC buy"}
     },
     "recommendation": "STRONG BUY",
     "timestamp": "2025-10-31T20:00:00Z"
   }
2. TRITON receives message and reviews research package
3. ARIA waits for TRITON decision on execution channel""",
    "domain": "event_bus",
    "task": "opportunity_alert"
})

corpus.append({
    "text": """Task: Subscribe to social sentiment updates from HYDRA

ARIA Action:
1. Subscribe to channel: ocean:social
2. Receive message: {
     "type": "SOCIAL_SPIKE",
     "symbol": "ETH",
     "galaxy_score": 82,
     "delta": "+35%",
     "sentiment": "VERY_BULLISH",
     "source": "HYDRA"
   }
3. Cross-reference with technical data from Ocean Scanner
4. If confluence detected, escalate to TRITON""",
    "domain": "event_bus",
    "task": "social_monitoring"
})

# === SECTION 6: CROSS-AI COORDINATION ===
print("[6/7] Cross-AI coordination workflows...")

corpus.append({
    "text": """Task: Coordinate with SAGE for news impact analysis

ARIA Workflow:
1. Detect technical breakout on BTC (Ocean Scanner)
2. Query SAGE via event bus: "Recent news for BTC past 4 hours?"
3. SAGE responds: "SEC Chairman hints at ETF approval in Q4"
4. ARIA correlates: Technical breakout + bullish news = STRONG signal
5. Calculate lead delta: News broke 1.2 hours before price move
6. Generate research package with news correlation for TRITON""",
    "domain": "cross_ai_coordination",
    "task": "sage_collaboration"
})

corpus.append({
    "text": """Task: Request meme virality assessment from DIONYSUS

ARIA Workflow:
1. Detect social spike on $PEPE (HYDRA alert)
2. Technical shows volume surge (Ocean Scanner)
3. Query DIONYSUS: "Assess $PEPE virality and scam risk"
4. DIONYSUS responds: "Tier: MOMENTUM, Security: CLEAR, Holders: 8.5K growing"
5. ARIA synthesizes: Social + Technical + Security = MEDIUM confidence meme play
6. Recommend to TRITON with 6-12 hour hold strategy""",
    "domain": "cross_ai_coordination",
    "task": "dionysus_collaboration"
})

# === SECTION 7: DECISION WORKFLOWS ===
print("[7/7] Complete decision-making workflows...")

corpus.append({
    "text": """Task: Full trading opportunity analysis workflow

ARIA Complete Process:
1. TRIGGER: HYDRA alerts social spike on SOL (+48% galaxy score)
2. TECHNICAL CHECK: Query Ocean Scanner
   - SOL RSI: 55 (good momentum)
   - MACD: Bullish crossover 2h ago
   - Volume: +62% above average
3. NEWS CHECK: Query SAGE via event bus
   - Breaking: Solana announces major DeFi partnership
4. BACKTEST: Call Trident for SOL strategies
   - Best: RSI_14_30_70 (22% return, 71% win rate) STAMPED
5. CONFLUENCE SCORING:
   - Technical: BULLISH (3/3 indicators)
   - Social: VERY BULLISH (high galaxy score + volume)
   - News: BULLISH (positive catalyst)
   - Confluence: 3/3 = 95% confidence
6. LEAD DELTA: Social spiked 3.1 hours before news (predictive)
7. GENERATE RESEARCH PACKAGE:
   - Symbol: SOL
   - Action: STRONG BUY
   - Entry: Current price
   - Stop loss: 5% below
   - Take profit: 15% above (based on backtest)
   - Confidence: 95%
   - Time horizon: 24-48 hours
8. PUBLISH to ocean:confluence for TRITON review
9. MONITOR position if executed, alert on stop/target hit""",
    "domain": "complete_workflow",
    "task": "full_analysis"
})

# Save corpus
print(f"\n\nSaving {len(corpus)} ARIA system-aware training samples...")
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    for item in corpus:
        f.write(json.dumps(item) + '\n')

print("\n" + "=" * 70)
print(f"ARIA SYSTEM CORPUS READY: {len(corpus)} samples")
print(f"Output: {OUTPUT_FILE}")
print("\nDomains covered:")
print("  - Ocean Scanner API usage")
print("  - Trident backtesting workflows")
print("  - TAAPI indicator interpretation")
print("  - Multi-source confluence detection")
print("  - Event bus messaging")
print("  - Cross-AI coordination")
print("  - Complete decision workflows")
print("=" * 70)
