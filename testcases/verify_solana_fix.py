import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()
SOLANA_API_KEY = os.getenv('SOLANA_API_KEY')
ADDRESS = "ETpvxQ95mN2d6Xiob8tnrCRQvSZrNDA3UgFEzd1oaFF5"

def test_rpc():
    print("\n--- Testing RPC getSignaturesForAddress ---")
    url = "https://api.mainnet-beta.solana.com"
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [
            ADDRESS,
            {"limit": 5}
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    
    with open("testcases/solana_fix_results.txt", "w") as f:
        f.write("TEST START\n")
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            f.write(f"RPC Status: {resp.status_code}\n")
            if resp.status_code == 200:
                data = resp.json()
                if 'result' in data:
                    f.write(f"RPC Result Count: {len(data['result'])}\n")
                else:
                    f.write(f"RPC Error Body: {json.dumps(data)}\n")
            else:
                f.write(f"RPC Failed Body: {resp.text[:200]}\n")
        except Exception as e:
            f.write(f"RPC Exception: {e}\n")

def test_solscan_utils():
    urls = [
        "https://public-api.solscan.io/utils/v2/account/transactions",
        "https://public-api.solscan.io/v2/account/transactions",
        "https://api.solscan.io/v2/account/transactions", 
        "https://api-v2.solscan.io/v2/account/transactions"
    ]
    
    headers = {"token": SOLANA_API_KEY, "User-Agent": "Mozilla/5.0"}
    
    with open("testcases/solana_fix_results.txt", "a") as f:
        for u in urls:
            try:
                resp = requests.get(f"{u}?address={ADDRESS}&limit=5", headers=headers, timeout=5)
                f.write(f"Testing {u}: Status {resp.status_code}\n")
                if resp.status_code == 200:
                    f.write(f"  SUCCESS Body: {resp.text[:200]}\n")
            except Exception as e:
                f.write(f"Testing {u}: Error {e}\n")

if __name__ == "__main__":
    test_rpc()
    test_solscan_utils()
