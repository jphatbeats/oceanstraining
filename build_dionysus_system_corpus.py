"""
DIONYSUS SYSTEM-AWARE TRAINING CORPUS BUILDER
Teaches DIONYSUS how to use meme + on-chain infrastructure:
- LunarCrush API (CRITICAL: galaxy_score, alt_rank, social metrics)
- GoPlus security API
- DexScreener DEX metrics
- Meme classification system
- Wallet analysis patterns
- Event bus alerts
"""

import json
from pathlib import Path

print("=" * 70)
print("BUILDING DIONYSUS SYSTEM-AWARE TRAINING CORPUS")
print("=" * 70)

OUTPUT_DIR = Path("N:/OCEANS/oceans_training/datasets/dionysus_meme_intelligence")
OUTPUT_FILE = OUTPUT_DIR / "training_corpus.jsonl"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

corpus = []

# === SECTION 1: LUNARCRUSH API (MOST CRITICAL) ===
print("\n[1/8] LunarCrush API knowledge (CRITICAL)...")

corpus.append({
    "text": """Task: Analyze social sentiment using LunarCrush

DIONYSUS Action:
1. Query LunarCrush API: GET https://lunarcrush.com/api4/public/coins/BTC/v1
2. Parse critical metrics:
   - galaxy_score: 75 (0-100 scale, >70 = strong community engagement)
   - alt_rank: 1 (lower = more popular, BTC always rank 1)
   - sentiment: 4.2 (1-5 scale, >4 = very bullish)
   - social_volume: 125000 (mentions across platforms)
   - social_volume_24h_change: +45% (HUGE spike = attention surge)
3. Interpretation: VERY BULLISH social setup
4. Action: Alert ARIA for confluence check with technical""",
    "domain": "lunarcrush_api",
    "task": "social_analysis"
})

corpus.append({
    "text": """Task: Detect social momentum shifts with LunarCrush

DIONYSUS Process:
1. Monitor galaxy_score trends for PEPE:
   - 48h ago: galaxy_score 35
   - 24h ago: galaxy_score 52 (+17 points)
   - Now: galaxy_score 68 (+16 points)
2. Social velocity calculation: +33 points in 48h = RAPID GROWTH
3. Check alt_rank movement:
   - 48h ago: rank 450
   - Now: rank 287 (moved up 163 spots = TRENDING)
4. Social volume: +180% in 24h (viral spread detected)
5. Classification: MOMENTUM tier meme (6-12 hour play)
6. Action: Send high-priority alert to TRITON""",
    "domain": "lunarcrush_api",
    "task": "momentum_detection"
})

corpus.append({
    "text": """Task: Compare social metrics across meme coins

DIONYSUS Batch Analysis:
1. Query LunarCrush for top 50 alt_rank coins
2. Filter for memes (PEPE, SHIB, DOGE, FLOKI, etc.)
3. Rank by galaxy_score:
   - PEPE: galaxy_score 72, alt_rank 145, sentiment 4.3 (TOP PICK)
   - SHIB: galaxy_score 65, alt_rank 178, sentiment 3.8 (GOOD)
   - FLOKI: galaxy_score 48, alt_rank 320, sentiment 3.2 (WEAK)
4. Social volume comparison: PEPE +220%, SHIB +45%, FLOKI -12%
5. Recommendation: Focus on PEPE (best combination of metrics)""",
    "domain": "lunarcrush_api",
    "task": "comparative_analysis"
})

# === SECTION 2: GOPLUS SECURITY API ===
print("[2/8] GoPlus security scanning...")

corpus.append({
    "text": """Task: Security audit new meme token

DIONYSUS Action:
1. Call GoPlus API: POST https://api.gopluslabs.io/api/v1/token_security/1
   Body: {"contract_addresses": ["0x123..."]}
2. Parse security flags:
   - is_honeypot: 0 (SAFE - can sell tokens)
   - is_open_source: 1 (contract verified)
   - owner_change_balance: 0 (owner cannot steal funds)
   - can_take_back_ownership: 0 (renounced)
   - buy_tax: 0.05 (5% tax acceptable)
   - sell_tax: 0.05 (5% tax acceptable, not honeypot)
   - holder_count: 2850 (decent distribution)
3. Security Score: 95/100 (CLEAR to trade)
4. Classification: LOW RISK""",
    "domain": "goplus_security",
    "task": "security_audit"
})

corpus.append({
    "text": """Task: Detect honeypot scam

DIONYSUS Detection:
1. GoPlus scan finds RED FLAGS:
   - is_honeypot: 1 (WARNING: cannot sell)
   - sell_tax: 0.99 (99% sell tax = RUG)
   - owner_change_balance: 1 (owner can drain)
   - holder_count: 45 (suspiciously low)
2. Security Score: 15/100 (SCAM DETECTED)
3. Classification: SCAM tier
4. Action: BLACKLIST token, warn TRITON if asked""",
    "domain": "goplus_security",
    "task": "scam_detection"
})

# === SECTION 3: DEXSCREENER DEX METRICS ===
print("[3/8] DexScreener DEX analysis...")

corpus.append({
    "text": """Task: Analyze DEX liquidity and volume

DIONYSUS Action:
1. Query DexScreener: GET https://api.dexscreener.com/latest/dex/tokens/0x123
2. Parse DEX metrics:
   - liquidity_usd: 850000 (good, >$500K = safer)
   - volume_24h: 1200000 (volume/liquidity ratio: 1.4x = healthy)
   - price_change_24h: +35% (strong upward movement)
   - txns_24h_buys: 1250 (high buyer activity)
   - txns_24h_sells: 380 (3:1 buy/sell ratio = BULLISH)
3. Bonding curve: 68% filled (approaching graduation)
4. Action: MOMENTUM tier, watch for 85% curve = graduation signal""",
    "domain": "dexscreener_api",
    "task": "dex_analysis"
})

corpus.append({
    "text": """Task: Detect pump.fun graduation timing

DIONYSUS Monitoring:
1. Track bonding curve: Currently at 82% (near graduation threshold)
2. Volume acceleration: +120% in last 4 hours
3. Holder growth: 500 new wallets in 2 hours
4. Liquidity adding: $200K added in last hour
5. Graduation signal: 85% curve hit = MIGRATION to Raydium DEX
6. Action: Alert TRITON for entry timing (buy before migration = 10-30% gain)""",
    "domain": "dexscreener_api",
    "task": "graduation_timing"
})

# === SECTION 4: WALLET ANALYSIS ===
print("[4/8] Wallet behavior patterns...")

corpus.append({
    "text": """Task: Analyze whale wallet activity

DIONYSUS Process:
1. Top 10 holder analysis:
   - Top holder: 8% (acceptable, not whale-dominated)
   - Top 10 combined: 28% (decentralized distribution)
   - Dev wallet: 3% (low, dev not dumping)
2. Recent transactions:
   - Whale buy: 50 ETH added 2 hours ago (BULLISH signal)
   - No large sells in 24h (whales holding)
3. Holder velocity: +180 new wallets in 6 hours (retail FOMO)
4. Classification: HEALTHY distribution, whale accumulation phase""",
    "domain": "wallet_analysis",
    "task": "whale_detection"
})

corpus.append({
    "text": """Task: Detect pump-and-dump wallet patterns

DIONYSUS Red Flags:
1. Top holder owns 45% (MASSIVE whale control)
2. Top 3 wallets control 72% (centralized, RUG RISK)
3. Dev wallet transferred 20% to exchanges 1h ago (DUMP INCOMING)
4. Holder count dropping: -120 wallets in 2h (people exiting)
5. Classification: RISKY / Potential RUG
6. Action: DO NOT TRADE, warn TRITON""",
    "domain": "wallet_analysis",
    "task": "rug_detection"
})

# === SECTION 5: MEME TIER CLASSIFICATION ===
print("[5/8] Meme classification system...")

corpus.append({
    "text": """Task: Classify meme coin into tier system

DIONYSUS Classification System:
- DIAMOND: Established memes (DOGE, SHIB), 6+ month holds
- MOMENTUM: Viral growth phase (6-12 hour holds)
- GRADUATION: Pump.fun → DEX migration plays (1-4 hour holds)
- RISKY: Unclear fundamentals, needs monitoring
- SCAM: Honeypot/rug detected, DO NOT TRADE

Current Token Analysis:
- LunarCrush: galaxy_score 68, alt_rank 245 (rising)
- Security: GoPlus 92/100 (clean)
- DEX: $850K liquidity, 1.4x volume ratio
- Holders: 2850, growing +15%/day
- Age: 8 days old

Classification: MOMENTUM tier
Hold strategy: 6-12 hours, take profit at 50-80% gain""",
    "domain": "meme_classification",
    "task": "tier_assignment"
})

# === SECTION 6: EVENT BUS ALERTS ===
print("[6/8] Event bus messaging...")

corpus.append({
    "text": """Task: Send meme opportunity alert to ARIA

DIONYSUS Action:
1. Publish to channel: ocean:memes
   Message: {
     "type": "MEME_OPPORTUNITY",
     "symbol": "PEPE",
     "tier": "MOMENTUM",
     "confidence": 0.78,
     "metrics": {
       "lunarcrush_galaxy_score": 72,
       "lunarcrush_alt_rank": 145,
       "sentiment": 4.3,
       "social_volume_change": "+220%",
       "security_score": 95,
       "liquidity_usd": 2100000,
       "holder_count": 8500
     },
     "recommendation": "BUY",
     "hold_time": "6-12 hours",
     "target_gain": "50-80%",
     "timestamp": "2025-10-31T20:00:00Z"
   }
2. ARIA receives alert and checks technical confluence
3. If aligned, escalates to TRITON""",
    "domain": "event_bus",
    "task": "meme_alert"
})

# === SECTION 7: CROSS-AI COORDINATION ===
print("[7/8] Cross-AI workflows...")

corpus.append({
    "text": """Task: Collaborate with ARIA for meme + technical confluence

DIONYSUS Workflow:
1. Detect PEPE social explosion (LunarCrush galaxy_score +20 in 4h)
2. Run security check (GoPlus): CLEAR
3. Send alert to ARIA via event bus
4. ARIA responds: "PEPE technical shows volume +180%, RSI 62 bullish"
5. DIONYSUS confirms: Social + Technical ALIGNED = HIGH CONFIDENCE
6. Generate joint recommendation to TRITON:
   - Entry: Current price
   - Strategy: MOMENTUM play (6-12h hold)
   - Take profit: 60% gain
   - Stop loss: 15% below entry""",
    "domain": "cross_ai_coordination",
    "task": "aria_collaboration"
})

# === SECTION 8: COMPLETE MEME ANALYSIS WORKFLOW ===
print("[8/8] Complete decision workflows...")

corpus.append({
    "text": """Task: Full meme coin evaluation workflow

DIONYSUS Complete Process:
1. TRIGGER: New token trending on pump.fun ($BONK)
2. LUNARCRUSH CHECK:
   - galaxy_score: 58 (medium-strong)
   - alt_rank: 380 (decent)
   - sentiment: 4.1 (bullish)
   - social_volume: +340% in 6h (VIRAL)
3. SECURITY AUDIT (GoPlus):
   - is_honeypot: 0 (SAFE)
   - Security score: 88/100 (CLEAR)
4. DEX METRICS (DexScreener):
   - Liquidity: $420K (acceptable)
   - Volume 24h: $850K (2x liquidity = healthy)
   - Bonding curve: 72% (graduation watch)
   - Buy/sell ratio: 4:1 (strong demand)
5. WALLET ANALYSIS:
   - Top holder: 12% (acceptable)
   - Top 10: 38% (decent distribution)
   - Holder count: 3200 (growing +18%/hour)
6. TIER CLASSIFICATION: MOMENTUM
7. CONFLUENCE CHECK:
   - LunarCrush: BULLISH
   - Security: CLEAR
   - DEX: HEALTHY
   - Wallets: ACCUMULATION
8. GENERATE RECOMMENDATION:
   - Symbol: $BONK
   - Tier: MOMENTUM
   - Action: BUY
   - Confidence: 78%
   - Hold: 6-12 hours
   - Entry: Current
   - Target: +60%
   - Stop: -15%
9. PUBLISH to ocean:memes for ARIA + TRITON
10. MONITOR: Watch for graduation at 85% bonding curve""",
    "domain": "complete_workflow",
    "task": "full_meme_analysis"
})

# Save corpus
print(f"\n\nSaving {len(corpus)} DIONYSUS system-aware training samples...")
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    for item in corpus:
        f.write(json.dumps(item) + '\n')

print("\n" + "=" * 70)
print(f"DIONYSUS SYSTEM CORPUS READY: {len(corpus)} samples")
print(f"Output: {OUTPUT_FILE}")
print("\nDomains covered:")
print("  - LunarCrush API (galaxy_score, alt_rank, sentiment) *** CRITICAL ***")
print("  - GoPlus security audits")
print("  - DexScreener DEX metrics")
print("  - Wallet behavior analysis")
print("  - Meme tier classification")
print("  - Event bus alerts")
print("  - Cross-AI coordination")
print("  - Complete meme analysis workflows")
print("=" * 70)
