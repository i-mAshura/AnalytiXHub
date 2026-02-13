
import os
import sys
from dotenv import load_dotenv

# Ensure modules can be imported
sys.path.append(os.getcwd())

from modules.fetchers.multi_chain import EtherscanMultiChainFetcher, SolanaFetcher

load_dotenv()

def test_etherscan_fetcher():
    print("\n[TEST] EtherscanMultiChainFetcher")
    api_key = os.getenv("ETHERSCAN_API_KEY")
    if not api_key:
        print("SKIP: ETHERSCAN_API_KEY not found")
        return

    # Use a known address (Vitalik's)
    address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    chain = "ethereum"
    
    try:
        # Test fetch_transactions with include_token_transfers (was causing TypeError)
        print(f"Fetching transactions for {address} on {chain}...")
        txs, counts = EtherscanMultiChainFetcher.fetch_transactions(
            chain=chain,
            address=address,
            include_internal=False, # Faster
            include_token_transfers=True 
        )
        print(f"SUCCESS: Fetched {len(txs)} transactions.")
        print(f"Counts: {counts}")
    except TypeError as e:
        print(f"FAIL: TypeError: {e}")
    except Exception as e:
        print(f"FAIL: Exception: {e}")

def test_solana_fetcher():
    print("\n[TEST] SolanaFetcher")
    api_key = os.getenv("SOLANA_API_KEY")
    if not api_key:
        print("SKIP: SOLANA_API_KEY not found")
        return

    # Use a known Solana address (Foundation or large wallet)
    # 5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1 (Example)
    address = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
    
    try:
        print(f"Fetching transactions for {address} on solana...")
        txs, counts = SolanaFetcher.fetch_transactions(address)
        print(f"SUCCESS: Fetched {len(txs)} transactions.")
        print(f"First tx: {txs[0] if txs else 'None'}")
    except Exception as e:
        print(f"FAIL: Exception: {e}")

if __name__ == "__main__":
    test_etherscan_fetcher()
    test_solana_fetcher()
