import sys
import os
sys.path.append(os.getcwd())
from modules.fetchers.multi_chain import SolanaFetcher
import json

def test_solana():
    # Whale address found in search
    address = "52C9T2T7JRojtxumYnYZhyUmrN7kqzvCLc4Ksvjk7TxD"
    print(f"Testing Solana fetch for: {address}")
    
    try:
        txs, counts = SolanaFetcher.fetch_transactions(address)
        print(f"Status: {counts}")
        if txs:
            print(f"First transaction found: {json.dumps(txs[0], indent=2)}")
            print(f"Total found: {len(txs)}")
        else:
            print("No transactions found.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_solana()
