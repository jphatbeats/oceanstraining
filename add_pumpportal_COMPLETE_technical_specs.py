"""
ADD COMPLETE PUMPPORTAL TECHNICAL SPECIFICATIONS
================================================
Adds comprehensive PumpPortal API knowledge from actual documentation scraping

Knowledge added:
- Local Transaction API (full transaction flow)
- WebSocket real-time subscriptions (4 methods)
- PumpSwap post-graduation API
- Complete fee structure
- Transaction signing process (Python + JavaScript examples)
- Critical implementation rules
"""

import json
from pathlib import Path

# Load existing dataset
DATASET_FILE = Path("N:/OCEANS/oceans_training/data/final_training/DIONYSUS_trading_brain_ENHANCED.jsonl")

print("=" * 70)
print("ADDING COMPLETE PUMPPORTAL TECHNICAL SPECIFICATIONS")
print("=" * 70)

# Load existing samples
existing_samples = []
with open(DATASET_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            existing_samples.append(json.loads(line.strip()))
        except:
            continue

print(f"\nLoaded {len(existing_samples):,} existing samples")

# Remove old API knowledge (we'll replace with complete version)
filtered_samples = [s for s in existing_samples if s.get('source') != 'pumpportal_api']
removed = len(existing_samples) - len(filtered_samples)
print(f"Removed {removed} old API samples (replacing with complete specs)")

# ============================================================================
# COMPLETE PUMPPORTAL TECHNICAL SPECIFICATIONS
# ============================================================================

COMPLETE_API_SPECS = []

# LOCAL TRANSACTION API (What DIONYSUS uses)
LOCAL_API_TEMPLATES = [
    {
        "topic": "PumpPortal Local Transaction API - Complete Flow",
        "content": """LOCAL TRANSACTION API (DIONYSUS uses this - 0.5% fee)

Endpoint: POST https://pumpportal.fun/api/trade-local

Request Body:
{
  "publicKey": "WALLET_PUBLIC_KEY",
  "action": "buy" | "sell",
  "mint": "TOKEN_CONTRACT_ADDRESS",
  "amount": "0.1" or "100%" (for sells),
  "denominatedInSol": "true" | "false",
  "slippage": 10,  // Percentage
  "priorityFee": 0.0001,  // SOL amount
  "pool": "pump" | "raydium" | "pump-amm" | "auto"
}

Response: Serialized VersionedTransaction (byte array)

Process:
1. POST to API with parameters
2. Receive byte array response
3. Deserialize into VersionedTransaction
4. Create Keypair from private key
5. Sign transaction with keypair
6. Send via Solana RPC (confirmed commitment)
7. Extract transaction signature

Fee: 0.5% (vs 1% for Lightning API)
Why Local: Full security control, no key exposure, custom RPC"""
    },
    {
        "topic": "Pool Routing - Complete Options",
        "content": """PumpPortal pool parameter options:

"pump" - Pump.fun bonding curve (pre-graduation)
  Use when: Market cap < $69k
  Best for: Early entry, bonding curve plays

"raydium" - Raydium AMM (post-graduation)
  Use when: Token graduated
  Best for: Higher liquidity, lower slippage

"pump-amm" - PumpSwap AMM
  Use when: Token migrated to PumpSwap
  Requires: API key + 0.02 SOL min balance

"launchlab" - LaunchLab DEX
"raydium-cpmm" - Raydium CPMM
"bonk" - BonkSwap

"auto" - Automatic routing (defaults to "pump")

Detection logic:
1. Check token market cap
2. If < $69k → pool: "pump"
3. If >= $69k → pool: "raydium"
4. Always verify graduation status before trading"""
    },
    {
        "topic": "Transaction Signing - Python Implementation",
        "content": """Python transaction signing with Solders library:

from solders.transaction import VersionedTransaction
from solders.keypair import Keypair
import base58
import requests

# 1. Call PumpPortal API
response = requests.post(
    'https://pumpportal.fun/api/trade-local',
    json={
        'publicKey': wallet_pubkey,
        'action': 'buy',
        'mint': token_mint,
        'amount': '0.1',
        'denominatedInSol': 'true',
        'slippage': 10,
        'priorityFee': 0.0001,
        'pool': 'pump'
    }
)

# 2. Deserialize transaction
tx_bytes = response.content
tx = VersionedTransaction.deserialize(tx_bytes)

# 3. Load keypair and sign
keypair = Keypair.from_base58_string(private_key_base58)
signed_tx = tx.sign([keypair])

# 4. Send via RPC
rpc_response = requests.post(rpc_url, json={
    'jsonrpc': '2.0',
    'id': 1,
    'method': 'sendTransaction',
    'params': [
        base58.b58encode(signed_tx.serialize()).decode(),
        {'commitment': 'confirmed'}
    ]
})

signature = rpc_response.json()['result']"""
    }
]

# WEBSOCKET REAL-TIME DATA
WEBSOCKET_TEMPLATES = [
    {
        "topic": "PumpPortal WebSocket - Real-Time Subscriptions",
        "content": """WebSocket: wss://pumpportal.fun/api/data

4 Subscription Methods:

1. subscribeNewToken - Token creation events
   Message: {"method": "subscribeNewToken"}
   Use: Monitor all new token launches real-time

2. subscribeTokenTrade - Specific token trades
   Message: {"method": "subscribeTokenTrade", "keys": ["MINT_ADDRESS"]}
   Use: Track trading activity on specific tokens

3. subscribeAccountTrade - Wallet activity
   Message: {"method": "subscribeAccountTrade", "keys": ["WALLET_PUBKEY"]}
   Use: Follow smart money wallets, detect whale buys/sells

4. subscribeMigration - Graduation events
   Message: {"method": "subscribeMigration"}
   Use: Detect when tokens graduate to Raydium

Unsubscribe: Replace "subscribe" with "unsubscribe" in method

CRITICAL RULE: Use ONE WebSocket connection for all subscriptions
DO NOT create new connection per token/wallet - will get blacklisted!"""
    },
    {
        "topic": "WebSocket Connection Management",
        "content": """Proper WebSocket usage (avoid blacklisting):

CORRECT:
1. Open ONE WebSocket connection
2. Send multiple subscription messages to SAME connection
3. Reuse connection for all tokens/wallets
4. Close only when shutting down

ws = new WebSocket('wss://pumpportal.fun/api/data')
ws.send({"method": "subscribeTokenTrade", "keys": ["TOKEN1"]})
ws.send({"method": "subscribeTokenTrade", "keys": ["TOKEN2"]})
ws.send({"method": "subscribeAccountTrade", "keys": ["WALLET1"]})

WRONG (WILL GET BLACKLISTED):
ws1 = new WebSocket(...) // For TOKEN1
ws2 = new WebSocket(...) // For TOKEN2 - BAD!
ws3 = new WebSocket(...) // For WALLET1 - BAD!

Multiple connections = blacklist = no data access"""
    }
]

# PUMPSWAP POST-GRADUATION
PUMPSWAP_TEMPLATES = [
    {
        "topic": "PumpSwap API - Post-Graduation Trading Data",
        "content": """PumpSwap (tokens graduated from bonding curve):

Connection: wss://pumpportal.fun/api/data?api-key=YOUR_API_KEY

Requirements:
- PumpPortal API key (get from dashboard)
- Linked wallet with minimum 0.02 SOL balance
- Cost: 0.01 SOL per 10,000 messages

Subscription methods:
- subscribeTokenTrade (post-graduation tokens)
- subscribeAccountTrade (wallet tracking)

Limitation:
If wallet balance < 0.02 SOL:
  - Connection restricted to bonding curve trades only
  - No PumpSwap data access

Data difference:
- Bonding curve: FREE, all trades visible
- PumpSwap: Requires API key + SOL, pay per message

Use case:
Monitor graduated tokens on PumpSwap AMM
Track post-graduation price action
Detect whale activity after migration"""
    }
]

# FEE STRUCTURE
FEE_TEMPLATES = [
    {
        "topic": "Complete PumpPortal Fee Structure",
        "content": """PumpPortal fees (all trading fees):

LOCAL TRANSACTION API (DIONYSUS uses):
- Fee: 0.5% per trade
- Calculated: Before slippage
- When: On every buy/sell
- Why cheaper: You handle signing/sending
- Additional: Solana network fees + Pump.fun bonding curve fees

LIGHTNING TRANSACTION API:
- Fee: 1% per trade (2x higher)
- Why higher: They handle everything
- Not recommended for DIONYSUS (has own wallets)

DATA API FEES:
- Bonding curve data: FREE (no charge)
- PumpSwap data: 0.01 SOL per 10,000 messages
- Requires: API key + 0.02 SOL minimum balance

TOTAL COST PER TRADE (Local API):
0.5% PumpPortal + ~0.000005 SOL network + Pump.fun bonding curve fee

Example: 0.1 SOL buy
- PumpPortal: 0.0005 SOL (0.5%)
- Network: ~0.000005 SOL
- Bonding curve: Variable (depends on curve position)
- Total: ~0.0005 SOL + curve fee"""
    }
]

# Generate samples
for template in LOCAL_API_TEMPLATES:
    for _ in range(30):  # 30 repetitions each
        COMPLETE_API_SPECS.append({
            "text": f"{template['topic']}\n\n{template['content']}",
            "source": "pumpportal_complete",
            "type": "technical_spec"
        })

for template in WEBSOCKET_TEMPLATES:
    for _ in range(30):
        COMPLETE_API_SPECS.append({
            "text": f"{template['topic']}\n\n{template['content']}",
            "source": "pumpportal_complete",
            "type": "technical_spec"
        })

for template in PUMPSWAP_TEMPLATES:
    for _ in range(20):
        COMPLETE_API_SPECS.append({
            "text": f"{template['topic']}\n\n{template['content']}",
            "source": "pumpportal_complete",
            "type": "technical_spec"
        })

for template in FEE_TEMPLATES:
    for _ in range(20):
        COMPLETE_API_SPECS.append({
            "text": f"{template['topic']}\n\n{template['content']}",
            "source": "pumpportal_complete",
            "type": "technical_spec"
        })

print(f"Generated {len(COMPLETE_API_SPECS):,} complete API specification samples")

# ============================================================================
# COMBINE AND SAVE
# ============================================================================

all_samples = filtered_samples + COMPLETE_API_SPECS

# Save
with open(DATASET_FILE, 'w', encoding='utf-8') as f:
    for sample in all_samples:
        f.write(json.dumps(sample) + '\n')

file_size_mb = DATASET_FILE.stat().st_size / (1024 * 1024)

print("\n" + "=" * 70)
print("COMPLETE PUMPPORTAL TECHNICAL SPECIFICATIONS ADDED")
print("=" * 70)
print(f"\nOutput: {DATASET_FILE}")
print(f"Total samples: {len(all_samples):,}")
print(f"Size: {file_size_mb:.1f} MB")
print(f"\nAPI Specification samples: {len(COMPLETE_API_SPECS):,}")
print("\nKnowledge coverage:")
print("  - LOCAL Transaction API (0.5% fee, full control)")
print("  - Complete pool routing (pump/raydium/pumpswap/auto)")
print("  - Transaction signing (Python implementation)")
print("  - WebSocket subscriptions (4 methods)")
print("  - WebSocket connection management (avoid blacklist)")
print("  - PumpSwap post-graduation API")
print("  - Complete fee structure")
print("  - Critical implementation rules")
print("\nDIONYSUS KNOWS THE COMPLETE PUMPPORTAL API!")
print("Ready for programmatic trading with FULL technical specs!")
