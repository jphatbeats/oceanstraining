"""
ADD EXACT PUMPPORTAL CODE EXAMPLES
===================================
Adds the ACTUAL working Python code from PumpPortal documentation

These are PRODUCTION-READY code examples DIONYSUS can use directly
"""

import json
from pathlib import Path

# Load existing dataset
DATASET_FILE = Path("N:/OCEANS/oceans_training/data/final_training/DIONYSUS_trading_brain_ENHANCED.jsonl")

print("=" * 70)
print("ADDING EXACT PUMPPORTAL CODE EXAMPLES")
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

# ============================================================================
# EXACT CODE EXAMPLES FROM PUMPPORTAL DOCUMENTATION
# ============================================================================

CODE_EXAMPLES = []

# EXACT LOCAL TRANSACTION API CODE
LOCAL_TX_CODE = {
    "topic": "PumpPortal Local Transaction API - EXACT Python Code",
    "content": """EXACT working Python code for LOCAL Transaction API:

import requests
from solders.transaction import VersionedTransaction
from solders.keypair import Keypair
from solders.commitment_config import CommitmentLevel
from solders.rpc.requests import SendVersionedTransaction
from solders.rpc.config import RpcSendTransactionConfig

# Step 1: Request transaction from PumpPortal
response = requests.post(url="https://pumpportal.fun/api/trade-local", data={
    "publicKey": "Your public key here",
    "action": "buy",             # "buy" or "sell"
    "mint": "token CA here",     # contract address
    "amount": 100000,            # SOL or token amount
    "denominatedInSol": "false", # "true" for SOL, "false" for tokens
    "slippage": 10,              # percent slippage
    "priorityFee": 0.005,        # priority fee amount
    "pool": "auto"               # "pump", "raydium", "pump-amm", etc
})

# Step 2: Load keypair and create signed transaction
keypair = Keypair.from_base58_string("Your base 58 private key here")
tx = VersionedTransaction(VersionedTransaction.from_bytes(response.content).message, [keypair])

# Step 3: Configure and send transaction
commitment = CommitmentLevel.Confirmed
config = RpcSendTransactionConfig(preflight_commitment=commitment)
txPayload = SendVersionedTransaction(tx, config)

response = requests.post(
    url="Your RPC Endpoint here - Eg: https://api.mainnet-beta.solana.com/",
    headers={"Content-Type": "application/json"},
    data=SendVersionedTransaction(tx, config).to_json()
)

# Step 4: Extract signature
txSignature = response.json()['result']
print(f'Transaction: https://solscan.io/tx/{txSignature}')

CRITICAL: This is EXACTLY how DIONYSUS executes trades programmatically"""
}

# JITO BUNDLES CODE (MEV PROTECTION)
JITO_BUNDLE_CODE = {
    "topic": "Jito Bundles - MEV Protection with Multiple Wallets",
    "content": """Jito Bundles for MEV protection (up to 5 transactions):

import requests
import base58
from solders.transaction import VersionedTransaction
from solders.keypair import Keypair

# Load up to 5 wallets for bundle
signerKeypairs = [
    Keypair.from_base58_string("Wallet A base 58 private key here"),
    Keypair.from_base58_string("Wallet B base 58 private key here")
    # use up to 5 wallets
]

# Request bundle of transactions
response = requests.post(
    "https://pumpportal.fun/api/trade-local",
    headers={"Content-Type": "application/json"},
    json=[
        {
            "publicKey": str(signerKeypairs[0].pubkey()),
            "action": "buy",
            "mint": "2xHkesAQteG9yz48SDaVAtKdFU6Bvdo9sXS3uQCbpump",
            "denominatedInSol": "false",
            "amount": 1000,
            "slippage": 50,
            "priorityFee": 0.0001, # First tx priority fee = jito tip
            "pool": "pump"
        },
        {
            "publicKey": str(signerKeypairs[1].pubkey()),
            "action": "buy",
            "mint": "2xHkesAQteG9yz48SDaVAtKdFU6Bvdo9sXS3uQCbpump",
            "denominatedInSol": "false",
            "amount": 1000,
            "slippage": 50,
            "priorityFee": 0.0001, # Ignored after first tx
            "pool": "pump"
        }
        # up to 5 transactions
    ]
)

if response.status_code != 200:
    print("Failed to generate transactions.")
    print(response.reason)
else:
    encodedTransactions = response.json()
    encodedSignedTransactions = []
    txSignatures = []

    # Sign all transactions
    for index, encodedTransaction in enumerate(encodedTransactions):
        signedTx = VersionedTransaction(
            VersionedTransaction.from_bytes(base58.b58decode(encodedTransaction)).message,
            [signerKeypairs[index]]
        )
        encodedSignedTransactions.append(base58.b58encode(bytes(signedTx)).decode())
        txSignatures.append(str(signedTx.signatures[0]))

    # Send bundle to Jito
    jito_response = requests.post(
        "https://mainnet.block-engine.jito.wtf/api/v1/bundles",
        headers={"Content-Type": "application/json"},
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "sendBundle",
            "params": [encodedSignedTransactions]
        }
    )

    for i, signature in enumerate(txSignatures):
        print(f'Transaction {i}: https://solscan.io/tx/{signature}')

Use case: Bundle multiple buys to avoid front-running / sandwich attacks"""
}

# WEBSOCKET REAL-TIME CODE
WEBSOCKET_CODE = {
    "topic": "WebSocket Real-Time Subscriptions - EXACT Python Code",
    "content": """EXACT Python code for WebSocket subscriptions:

import asyncio
import websockets
import json

async def subscribe():
    uri = "wss://pumpportal.fun/api/data"
    async with websockets.connect(uri) as websocket:

        # Subscribe to NEW token creation events
        payload = {"method": "subscribeNewToken"}
        await websocket.send(json.dumps(payload))

        # Subscribe to token MIGRATION events (graduation)
        payload = {"method": "subscribeMigration"}
        await websocket.send(json.dumps(payload))

        # Subscribe to trades by SPECIFIC WALLETS (smart money tracking)
        payload = {
            "method": "subscribeAccountTrade",
            "keys": ["AArPXm8JatJiuyEffuC1un2Sc835SULa4uQqDcaGpAjV"]
        }
        await websocket.send(json.dumps(payload))

        # Subscribe to trades on SPECIFIC TOKENS
        payload = {
            "method": "subscribeTokenTrade",
            "keys": ["91WNez8D22NwBssQbkzjy4s2ipFrzpmn5hfvWVe2aY5p"]
        }
        await websocket.send(json.dumps(payload))

        # Listen for messages
        async for message in websocket:
            data = json.loads(message)
            print(data)

# Run
asyncio.get_event_loop().run_until_complete(subscribe())

CRITICAL: Use ONE WebSocket connection for ALL subscriptions
Reuse same 'websocket' object - DO NOT create new connections
Multiple connections = BLACKLIST"""
}

# WEBSOCKET UNSUBSCRIBE CODE
WEBSOCKET_UNSUB_CODE = {
    "topic": "WebSocket Unsubscribe - EXACT Python Code",
    "content": """Unsubscribe from WebSocket data streams:

import asyncio
import websockets
import json

async def subscribe():
    uri = "wss://pumpportal.fun/api/data"
    async with websockets.connect(uri) as websocket:

        # Subscribe to new token events
        payload = {"method": "subscribeNewToken"}
        await websocket.send(json.dumps(payload))

        # ... later, unsubscribe
        payload = {"method": "unsubscribeNewToken"}
        await websocket.send(json.dumps(payload))

        async for message in websocket:
            print(json.loads(message))

# Unsubscribe methods:
# - unsubscribeNewToken
# - unsubscribeTokenTrade
# - unsubscribeAccountTrade

Use case: Stop monitoring tokens that graduated or became inactive"""
}

# PUMPSWAP API CODE
PUMPSWAP_CODE = {
    "topic": "PumpSwap Data API - EXACT Python Code (Post-Graduation)",
    "content": """PumpSwap API for post-graduation tokens:

import asyncio
import websockets
import json

async def subscribe():
    # Include API key in URL
    uri = "wss://pumpportal.fun/api/data?api-key=your-api-key-here"
    async with websockets.connect(uri) as websocket:

        # Subscribe to wallet trades (works on PumpSwap)
        payload = {
            "method": "subscribeAccountTrade",
            "keys": ["AArPXm8JatJiuyEffuC1un2Sc835SULa4uQqDcaGpAjV"]
        }
        await websocket.send(json.dumps(payload))

        # Subscribe to token trades (works on PumpSwap)
        payload = {
            "method": "subscribeTokenTrade",
            "keys": ["token_contract_address"]
        }
        await websocket.send(json.dumps(payload))

        async for message in websocket:
            print(json.loads(message))

Requirements:
- PumpPortal API key
- Linked wallet with >= 0.02 SOL
- Cost: 0.01 SOL per 10,000 messages

If balance < 0.02 SOL:
  - Connection restricted to bonding curve trades only
  - No PumpSwap data access

Use case: Monitor graduated tokens on PumpSwap AMM"""
}

# CREATE WALLET CODE
CREATE_WALLET_CODE = {
    "topic": "Programmatic Wallet Creation - EXACT Python Code",
    "content": """Create new wallets and API keys programmatically:

import requests

# Create new wallet + linked API key
response = requests.get(url="https://pumpportal.fun/api/create-wallet")

# Returns JSON with:
# - New wallet public key
# - New wallet private key
# - Linked PumpPortal API key
data = response.json()

wallet_pubkey = data['publicKey']
wallet_privkey = data['privateKey']
api_key = data['apiKey']

Use case:
- Generate wallets for DIONYSUS HOT/BUFFER/RESERVE system
- Create separate trading wallets for risk isolation
- Generate API keys for PumpSwap data access"""
}

# Generate samples (30 repetitions each for emphasis)
all_code_templates = [
    LOCAL_TX_CODE,
    JITO_BUNDLE_CODE,
    WEBSOCKET_CODE,
    WEBSOCKET_UNSUB_CODE,
    PUMPSWAP_CODE,
    CREATE_WALLET_CODE
]

for template in all_code_templates:
    for _ in range(30):  # Repeat 30x to BURN INTO WEIGHTS
        CODE_EXAMPLES.append({
            "text": f"{template['topic']}\n\n{template['content']}",
            "source": "pumpportal_exact_code",
            "type": "production_code"
        })

print(f"Generated {len(CODE_EXAMPLES):,} exact code example samples")

# ============================================================================
# COMBINE AND SAVE
# ============================================================================

all_samples = existing_samples + CODE_EXAMPLES

# Save
with open(DATASET_FILE, 'w', encoding='utf-8') as f:
    for sample in all_samples:
        f.write(json.dumps(sample) + '\n')

file_size_mb = DATASET_FILE.stat().st_size / (1024 * 1024)

print("\n" + "=" * 70)
print("EXACT PUMPPORTAL CODE EXAMPLES ADDED")
print("=" * 70)
print(f"\nOutput: {DATASET_FILE}")
print(f"Total samples: {len(all_samples):,}")
print(f"Size: {file_size_mb:.1f} MB")
print(f"\nExact code samples: {len(CODE_EXAMPLES):,}")
print("\nCode coverage:")
print("  - LOCAL Transaction API (complete working code)")
print("  - Jito Bundles (MEV protection, up to 5 wallets)")
print("  - WebSocket subscriptions (async Python)")
print("  - WebSocket unsubscribe (connection management)")
print("  - PumpSwap API (post-graduation)")
print("  - Wallet creation (programmatic)")
print("\nDIONYSUS HAS PRODUCTION-READY CODE!")
print("These are EXACT examples from official documentation!")
print("DIONYSUS can literally copy-paste this code to execute trades!")
