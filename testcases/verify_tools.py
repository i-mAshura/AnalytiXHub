
import os
import sys
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.utils.visualizations import create_timeline_visualization, create_sankey_diagram, create_heatmap_visualization
from modules.analyzers.advanced_analysis import AddressClustering
from modules.utils.helpers import normalize_address

# Mock Data (Solana-style mixed case)
ROOT_ADDR = "H8smjscqxfkiftcfdr3dumlpwcrbm61lgfj8n4dk3w"
COUNTERPARTY = "Gjrs4fwhtemz5ze9x3fnvj8tmwitkth21yxdrpqn7np"

mock_txs = [
    {
        "hash": "tx1",
        "timestamp": "2024-01-01 12:00:00", # String timestamp
        "from": ROOT_ADDR,
        "to": COUNTERPARTY,
        "value": 1.5,
        "chain": "solana"
    },
    {
        "hash": "tx2",
        "timestamp": 1704110400, # Int timestamp
        "from": COUNTERPARTY,
        "to": ROOT_ADDR,
        "value": 2.0,
        "chain": "solana"
    }
]

mock_summary = {
    "top_victims": [(COUNTERPARTY, 2.0)],
    "top_suspects": [(COUNTERPARTY, 1.5)],
    "total_transactions": 2
}

def verify_tools():
    print("Verifying Forensic Tools...")
    
    # 1. Timeline
    print("1. Testing Timeline...")
    res = create_timeline_visualization(mock_txs, ROOT_ADDR, "test_timeline.html")
    if res and os.path.exists(res):
        print("   PASS: Timeline generated.")
    else:
        print("   FAIL: Timeline generation failed.")

    # 2. Sankey
    print("2. Testing Sankey...")
    res = create_sankey_diagram(mock_summary, ROOT_ADDR, "test_sankey.html")
    if res and os.path.exists(res):
        print("   PASS: Sankey generated.")
    else:
        print("   FAIL: Sankey generation failed.")

    # 3. Heatmap
    print("3. Testing Heatmap...")
    res = create_heatmap_visualization(mock_txs, ROOT_ADDR, "test_heatmap.png")
    if res and os.path.exists(res):
        print("   PASS: Heatmap generated.")
    else:
        print("   FAIL: Heatmap generation failed.")

    # 4. Clustering (Case Sensitivity)
    print("4. Testing Clustering (Solana Case Sensitivity)...")
    
    # Verify normalize_address logic with negative ID (Solana = -1)
    norm_res = normalize_address("TestCase", -1)
    if norm_res == "TestCase":
        print("   PASS: normalize_address(-1) preserved case.")
    else:
        print(f"   FAIL: normalize_address(-1) returned {norm_res}")

    # Simulate app.py passing Solscan chain ID (e.g., 'solana' or specific ID if mapped)
    # logic in helpers.py treats 'solana' or negative IDs as non-EVM.
    # We'll pass chain_id='solana' effectively
    clusters = AddressClustering.cluster_addresses(mock_txs, ROOT_ADDR, chain_id="solana")
    
    # Check internal graph keys
    print(f"   Clusters found: {clusters.keys()}")
    
    # We can't easily check the internal graph of AddressClustering without accessing private members 
    # but we can check if it crashed.
    print("   PASS: Clustering ran without error.")

if __name__ == "__main__":
    verify_tools()
