import os
import sys
from datetime import datetime

# Add project root to path
sys.path.append(os.getcwd())

from multi_chain import MultiChainFetcher
from ml_engine import ml_engine
from breadcrumbs_client import BreadcrumbsClient

def test_multichain():
    print("\n--- Testing MultiChain APIs ---")
    
    # BTC (Mempool)
    print("1. Testing Bitcoin (Mempool)...")
    btc_addr = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa" # Genesis
    txs, _ = MultiChainFetcher.fetch_by_chain('bitcoin', btc_addr)
    print(f"BTC Txs: {len(txs)}")
    if len(txs) > 0: print("✅ BTC Success")
    else: print("❌ BTC Failed (or empty)")

    # SOL (Solscan)
    print("\n2. Testing Solana (Solscan)...")
    sol_addr = "5hn5mIxRxc7s3... (Mock)" # Need a real address or just test the function
    # Using a known active address (Binance Cold Wallet or similar)
    sol_addr = "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM" 
    txs, _ = MultiChainFetcher.fetch_by_chain('solana', sol_addr)
    print(f"SOL Txs: {len(txs)}")
    if len(txs) > 0: print("✅ SOL Success")
    else: print("❌ SOL Failed (or empty)")

    # TRON (TronGrid)
    print("\n3. Testing Tron (TronGrid)...")
    tron_addr = "TMuA6YqfCeX8EhbfYEg5y7S4DqzSJireY9" # USDT Contract or major wallet
    txs, _ = MultiChainFetcher.fetch_by_chain('tron', tron_addr)
    print(f"TRON Txs: {len(txs)}")
    if len(txs) > 0: print("✅ TRON Success")
    else: print("❌ TRON Failed (or empty)")

def test_ml_engine():
    print("\n--- Testing ML Engine ---")
    mock_txs = [
        {'value': 1.0, 'timestamp': '2024-01-01 10:00:00'},
        {'value': 1.2, 'timestamp': '2024-01-01 10:05:00'},
        {'value': 0.9, 'timestamp': '2024-01-01 10:10:00'},
        {'value': 500.0, 'timestamp': '2024-01-01 10:11:00'}, # Anomaly
        {'value': 1.1, 'timestamp': '2024-01-01 10:15:00'},
    ]
    
    anomalies = ml_engine.detect_anomalies(mock_txs)
    print(f"Detected {len(anomalies)} anomalies (Expected 1)")
    if len(anomalies) == 1 and anomalies[0]['value'] == 500.0:
        print("✅ ML Anomaly Detection Success")
    else:
        print("❌ ML Anomaly Detection Failed")

def test_breadcrumbs():
    print("\n--- Testing Breadcrumbs Client ---")
    client = BreadcrumbsClient(breadcrumbs_key="81CGNLRY9ICK6HOK5D52XIG6D7RXG5")
    # Using a known address
    data = client.get_graph_data("0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984", chain_id=1)
    print(f"Graph Elements: {len(data)}")
    if len(data) > 0: print("✅ Breadcrumbs (ETH) Success")
    else: print("❌ Breadcrumbs (ETH) Failed")

    # Testing Solana via Breadcrumbs (Should use Solscan)
    print("\n--- Testing Breadcrumbs Client (SOLANA Force) ---")
    # Solana Donation Address (Ukraine)
    sol_addr = "667m6yAxnBPHYvwCft4fDeR8ZIRs3w2s5wH2Y9y9tXh" 
    data_sol = client.get_graph_data(sol_addr, chain_id='solana')
    print(f"Graph Elements (SOL): {len(data_sol)}")
    # Root node is always 1. If fetch works, we should have edges/other nodes.
    if len(data_sol) > 1: 
        print(f"✅ Breadcrumbs (SOL) Success (Likely used Solscan). Found {len(data_sol)} elements.")
    else: 
        print("❌ Breadcrumbs (SOL) Failed (Only root node found or empty)")

if __name__ == "__main__":
    try:
        test_multichain()
        test_ml_engine()
        test_breadcrumbs()
        print("\n✅ Verification Complete")
    except Exception as e:
        print(f"\n❌ Verification Error: {e}")
