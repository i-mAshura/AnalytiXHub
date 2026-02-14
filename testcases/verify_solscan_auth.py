print("STARTING VERIFY SCRIPT")
import requests
import os
import json
from dotenv import load_dotenv

print("IMPORTS DONE. LOADING ENV...")
load_dotenv()

SOLANA_API_KEY = os.getenv('SOLANA_API_KEY')
ADDRESS = "ETpvxQ95mN2d6Xiob8tnrCRQvSZrNDA3UgFEzd1oaFF5"

print(f"API KEY LENGTH: {len(SOLANA_API_KEY) if SOLANA_API_KEY else 0}")

def test_variations():
    print("Beginning test_variations...")
    endpoints = [
        ("Pro v2", "https://pro-api.solscan.io/v2.0/account/transactions"),
        ("Public v2 (No v2 path)", "https://public-api.solscan.io/account/transactions"),
        ("Public v2 (With v2.0 path)", "https://public-api.solscan.io/v2.0/account/transactions"),
        ("Public v2 (With v2 path)", "https://api.solscan.io/v2/account/transactions"),
        ("Public v2 (Transfers)", "https://public-api.solscan.io/account/transfers"),
        ("Browser API", "https://api.solscan.io/account/transactions"),
    ]
    
    header_styles = [
        ("Bearer", {"Authorization": f"Bearer {SOLANA_API_KEY}"}),
        ("Token Header", {"token": SOLANA_API_KEY}),
        ("No Auth", {})
    ]

    with open("testcases/solscan_results_v2.txt", "w") as f:
        f.write("STARTING TESTS\n")

    for name, base_url in endpoints:
        print(f"--- Testing {name} ---")
        url = f"{base_url}?address={ADDRESS}&limit=5"
        
        for h_name, auth_headers in header_styles:
            print(f"  [Header: {h_name}] ", end="")
            
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            }
            if auth_headers: headers.update(auth_headers)
            
            try:
                resp = requests.get(url, headers=headers, timeout=5)
                result_str = f"Status: {resp.status_code}"
                print(result_str)
                
                with open("testcases/solscan_results_v2.txt", "a") as f:
                    f.write(f"Testing {name} with header {h_name}: {result_str}\n")
                    if resp.status_code == 200:
                         try:
                             data = resp.json()
                             item_count = len(data) if isinstance(data, list) else len(data.get('data', []) or [])
                             f.write(f"    SUCCESS! Items: {item_count}\n")
                         except:
                             f.write(f"    SUCCESS but invalid JSON\n")
                    else:
                         # Log body if short
                         body = resp.text[:200].replace('\n', ' ')
                         f.write(f"    Failed ({resp.status_code}) - Body: {body}\n")

            except Exception as e:
                print(f"    ❌ Request Error: {e}")
                with open("testcases/solscan_results_v2.txt", "a") as f:
                    f.write(f"Testing {name} with header {h_name}: Error {e}\n")

if __name__ == "__main__":
    test_variations()
