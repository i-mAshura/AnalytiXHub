
import requests
import time

address = "52C9T2T7JRojtxumYnYZhyUmrN7kqzvCLc4Ksvjk7TxD"

endpoints = [
    # V1 / Legacy
    f"https://public-api.solscan.io/account/transactions?account={address}&limit=10",
    f"https://api.solscan.io/account/transactions?address={address}&limit=10",
    f"https://api.solscan.io/account/solTransfers?account={address}&limit=10",
    f"https://public-api.solscan.io/account/solTransfers?account={address}&limit=10",
    # V2 Public?
    f"https://pro-api.solscan.io/v1.0/account/transactions?address={address}", # sometimes works without key?
    # RPC as fallback check
    "https://api.mainnet-beta.solana.com" 
]

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

print(f"Testing endpoints for {address}...")

for url in endpoints:
    print(f"\nTrying: {url}")
    try:
        if "mainnet-beta" in url:
            # RPC check
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getSignaturesForAddress",
                "params": [address, {"limit": 10}]
            }
            resp = requests.post(url, json=payload, headers=headers, timeout=5)
        else:
            resp = requests.get(url, headers=headers, timeout=5)
            
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            if "result" in data:
                 print("SUCCESS (RPC): Found result keys")
            elif isinstance(data, list) or "data" in data:
                 print("SUCCESS (API): Found data")
                 print(str(data)[:200])
                 break
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(1)
