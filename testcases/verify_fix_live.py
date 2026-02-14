import sys
import os
sys.path.append(os.getcwd())

from modules.fetchers.multi_chain import SolanaFetcher

ADDRESS = "ETpvxQ95mN2d6Xiob8tnrCRQvSZrNDA3UgFEzd1oaFF5"

print("Testing SolanaFetcher RPC Fallback with fix...")
try:
    txs, counts = SolanaFetcher._fetch_rpc_signatures(ADDRESS, limit=5)
    print(f"Status: Success")
    print(f"Count: {len(txs)}")
    if len(txs) > 0:
        print(f"Sample: {txs[0]['hash']}")
    else:
        print("Returned 0 transactions (Unexpected if RPC works)")
except Exception as e:
    print(f"Exception: {e}")
