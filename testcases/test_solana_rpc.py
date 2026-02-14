import requests
import json
import time

# Public RPC Endpoints (Official & reputable backups)
RPC_ENDPOINTS = [
    "https://solana-mainnet.rpc.extrnode.com",
    "https://api.devnet.solana.com",
    "https://api.mainnet-beta.solana.com",
]

ADDRESS = "667m6yAxnBPHYvwCft4fDeR8ZIRs3w2s5wH2Y9y9tXh"

def rpc_call(method, params):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params
    }
    
    print(f"DEBUG Payload: {json.dumps(payload)}")
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    
    for url in RPC_ENDPOINTS:
        try:
            print(f"Testing {url}...")
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'result' in data:
                    return data['result']
                else:
                    print(f"RPC Error: {data}")
            else:
                print(f"HTTP Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Connection Error: {e}")
    return None

def test_rpc_fetch():
    print(f"--- 0. Diagnostics: getSlot ---")
    slot = rpc_call("getSlot", [])
    if slot:
        print(f"Current Slot: {slot}")
    else:
        print("getSlot failed.")

    print(f"--- 0. Diagnostics: getHealth ---")
    health = rpc_call("getHealth", [])
    print(f"Health: {health}")

    print(f"\n--- 1. Fetching Signatures for {ADDRESS} (Minimal Params) ---")
    sigs = rpc_call("getSignaturesForAddress", [ADDRESS])
    
    if not sigs:
        print("Failed to fetch signatures.")
        return

    print(f"Found {len(sigs)} signatures.")
    print(f"Sample Signature: {sigs[0]['signature']}")

    print(f"\n--- 2. Fetching Transaction Details ---")
    tx_sig = sigs[0]['signature']
    
    # maxSupportedTransactionVersion=0 is needed for newer txs
    tx_details = rpc_call("getTransaction", [
        tx_sig, 
        {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}
    ])
    
    if not tx_details:
        print("Failed to fetch transaction details.")
        return
        
    print("Successfully fetched transaction details!")
    
    # Analyze Data for Parsing
    meta = tx_details.get('meta', {})
    txn = tx_details.get('transaction', {})
    msg = txn.get('message', {})
    
    print("\n[Meta Data Sample]:")
    print(f"PreBalances: {meta.get('preBalances')[:3]}...")
    print(f"PostBalances: {meta.get('postBalances')[:3]}...")
    
    print("\n[Token Balances]:")
    print(f"PreTokenBalances: {len(meta.get('preTokenBalances', []))}")
    print(f"PostTokenBalances: {len(meta.get('postTokenBalances', []))}")

    # Basic Flow Calc Logic Check
    # Account Keys are in msg['accountKeys']
    accounts = [a['pubkey'] for a in msg.get('accountKeys', [])]
    try:
        idx = accounts.index(ADDRESS)
        pre = meta['preBalances'][idx]
        post = meta['postBalances'][idx]
        change = (post - pre) / 1e9
        print(f"\nCalculated SOL Change for target: {change} SOL")
    except ValueError:
        print("\nTarget address not in account keys (should not happen for getSignaturesForAddress result)")

if __name__ == "__main__":
    test_rpc_fetch()
