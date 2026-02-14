
import os
import sys
import json
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.fetchers.multi_chain import SolanaFetcher

# The address the user is complaining about (in lowercase)
TARGET_ADDR = "h8smjscqxfkiftcfdr3dumlpwcrbm61lgfj8n4dk3wjs"

def debug_fetch():
    print(f"Fetching transactions for {TARGET_ADDR}...")
    try:
        txs, counts = SolanaFetcher.fetch_transactions(TARGET_ADDR)
        print(f"Fetched {len(txs)} transactions.")
        if len(txs) > 0:
            print("First 3 transactions:")
            for i, tx in enumerate(txs[:3]):
                print(f"--- TX {i+1} ---")
                print(f"Hash: {tx.get('hash')}")
                print(f"From: {tx.get('from')} (Type: {type(tx.get('from'))})")
                print(f"To:   {tx.get('to')} (Type: {type(tx.get('to'))})")
                
                # Check for casing
                frm = tx.get('from', '')
                to = tx.get('to', '')
                
                if frm == TARGET_ADDR:
                     print("-> 'from' matches input (lowercase).")
                elif frm.lower() == TARGET_ADDR:
                     print("-> 'from' is Mixed Case! (GOOD)")
                else:
                     print(f"-> 'from' is {frm}")
                     
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_fetch()
