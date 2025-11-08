"""PHASE 15 - Entity-Specific Prompt Templates - RunPod Optimized"""

ARIA_PROMPTS = [
    "Analyze the following technical indicators for BTC and identify any confluence signals: RSI=45, MACD crossing bullish, Volume increasing 20%. What patterns do you detect?",
    "Given these market conditions: ETH breaking resistance at $2,100, Bitcoin dominance at 52%, what technical opportunities exist?",
    "Evaluate this multi-timeframe setup: 1H shows bullish divergence, 4H MACD turning positive, Daily RSI oversold. What's your technical assessment?",
    "Identify correlation patterns between BTC price action and these altcoins: SOL +5%, AVAX +3%, MATIC +2%. What does this suggest?",
    "Analyze this breakout scenario: SOL volume 3x average, price above 20-day MA, RSI at 65. Is this a valid entry signal?",
    "Three sources align on AVAX: Ocean Scanner shows RSI divergence, LunarCrush galaxy score rising, news mentions increasing. What's the confluence score?",
    "Detect early signals in this data: BTC 1H candle volume spike, social mentions up 40%, no news catalyst. What might be forming?",
    "Map correlations: When BTC moves -2%, ETH typically moves -3%, but today ETH only dropped -1%. What does this divergence mean?",
    "Evaluate this opportunity: Technical breakout + positive social sentiment + sector rotation into L1s. Confidence level?",
    "Cross-reference these signals: TAAPI shows oversold on 3 timeframes, LunarCrush bearish sentiment. Is this a contrarian setup?",
]

DIONYSUS_PROMPTS = [
    "Analyze this tweet about $PEPE: 'PEPE to the moon! 🐸 Everyone's buying!'. Assess sentiment and viral potential.",
    "Evaluate meme coin $SHIB: 24h volume +150%, social mentions +200%, whale wallet activity detected. Viral score?",
    "This meme coin just launched with funny frog mascot, active Telegram (5k members), no audit. Classify the risk tier.",
    "Social sentiment shift detected: $DOGE mentions increased 5x in 2 hours, mostly positive emoji usage. What's happening?",
    "Predict virality: New meme token with cat theme, strong community memes, celebrity retweet. Will this trend?",
    "Wallet 0x1234...abcd just bought 500 ETH worth of $PEPE in 3 transactions. What does this signal?",
    "Meme coin $FLOKI showing: 100+ new wallets/hour, average hold time 6 hours, 30% wallets exiting. Interpret behavior.",
    "Early wallet accumulation pattern: 20 wallets bought within first hour, still holding after 48h. Significance?",
    "Detect the pump: Volume spike 10x, price +40% in 15 minutes, social mentions lagging. Real or coordinated?",
    "This meme coin graduated from Pump.fun to Raydium with $2M liquidity. What's the next 24h outlook?",
]

SAGE_PROMPTS = [
    "Analyze this headline: 'Federal Reserve hints at rate cut in Q2 2025'. Impact on crypto markets?",
    "Breaking news: 'Major exchange lists 3 new altcoins today'. Interpret significance for sector rotation.",
    "Macro event: 'US inflation data shows 2.8%, below expectations'. How does this affect risk assets like crypto?",
    "Read this article: 'Ethereum Layer 2 adoption reaches all-time high'. What are the second-order effects?",
    "Global context: 'China eases crypto mining restrictions in select provinces'. Long-term implications?",
    "Rate the impact of this news: 'Bitcoin ETF sees $500M inflow in single day'. Bullish/bearish and magnitude?",
    "Assess this regulatory headline: 'SEC approves spot Ethereum ETF applications'. Market impact timeline?",
    "Sentiment analysis: 'Crypto lending platform Celsius files for bankruptcy'. Contagion risk assessment?",
    "Connect macro to crypto: 'Tech stocks rally on AI optimism'. How does this flow into crypto sector?",
    "News cluster detected: 5 articles about DeFi security breaches today. Aggregate sentiment and sector impact?",
]

HYDRA_PROMPTS = [
    "Parse this Reddit post from r/CryptoCurrency: 'Just went all-in on ETH at $2k, am I late?'. Extract sentiment and position.",
    "Analyze Twitter thread: User claims inside info on upcoming Coinbase listing, 500 retweets. Credibility assessment?",
    "Telegram message from meme coin channel: '🚀🚀🚀 PUMP INCOMING! Dev team delivering!!'. Decode the signal.",
    "Discord community mood: 80% of recent messages contain sad emojis, complaints about price. Sentiment shift detected?",
    "Social narrative forming: 'Solana killer' mentioned 50+ times today across platforms. Track this narrative.",
    "Interpret crypto slang: 'Ser, this gem is a 100x, WAGMI, DYOR but I'm aping in'. What's the actual message?",
    "Detect sarcasm: 'Oh great, another -10% day. Love this for us. 🔥'. Real sentiment vs stated sentiment?",
    "Narrative shift: Last week everyone said 'bear market', now seeing 'accumulation phase'. What changed?",
    "Meme evolution: Pepe memes replaced by Wojak sad face memes in last 24h. Social mood indicator?",
    "Influencer analysis: Crypto Twitter account (500k followers) just flipped bearish. Potential impact?",
]

# FULL PRODUCTION - 48K total samples
SAMPLE_TARGETS = {
    "ARIA": {
        "finma": 5000,
        "finance_llm": 6000
    },
    "DIONYSUS": {
        "cryptobert": 5000,
        "finbert": 4000,
        "nemotron": 6000
    },
    "SAGE": {
        "finma": 5000,
        "finbert": 6000
    },
    "HYDRA": {
        "cryptobert": 6000,
        "finbert": 5000
    }
}

def get_prompts_for_entity(entity_name):
    """Get prompt list for a specific entity"""
    prompts = {
        "ARIA": ARIA_PROMPTS,
        "DIONYSUS": DIONYSUS_PROMPTS,
        "SAGE": SAGE_PROMPTS,
        "HYDRA": HYDRA_PROMPTS
    }
    return prompts.get(entity_name.upper(), [])

def get_sample_target(entity, donor):
    """Get target sample count for entity-donor pair"""
    return SAMPLE_TARGETS.get(entity, {}).get(donor, 1000)
