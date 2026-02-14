
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.fetchers.breadcrumbs_client import BreadcrumbsClient

def test_case_sensitivity():
    client = BreadcrumbsClient()
    
    # Test Cases
    cases = [
        ("ethereum", "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", "0xd8da6bf26964af9d7eed9e03e53415d37aa96045"), # EVM -> Lowercase
        ("solana", "Guip4x3g2h...MixedCase", "Guip4x3g2h...MixedCase"), # Solana -> Keep Case
        ("bitcoin", "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"), # BTC -> Keep Case
        ("tron", "T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb", "T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb") # Tron -> Keep Case
    ]
    
    print("[-] Testing Address Normalization Logic (Pre-Fix/Post-Fix)...")
    
    failed = False
    
    # Since we can't easily access the internal method before it exists, 
    # we will test the public method 'get_graph_data' and check the ID of the root node.
    
    for chain, addr_input, expected in cases:
        try:
            # We map chain name to ID for the client
            chain_id_map = {
                "ethereum": 1,
                "solana": -1,
                "bitcoin": 0,
                "tron": -2
            }
            chain_id = chain_id_map.get(chain)
            
            print(f"Testing {chain} ({chain_id}) with {addr_input}...")
            
            # Mocking fetch to avoid API calls? 
            # Actually, get_graph_data creates the root node *before* fetching.
            # So we can test it even without valid API keys for some.
            
            elements = client.get_graph_data(addr_input, chain_id=chain_id)
            
            # Find root node
            root_node = next((el for el in elements if 'classes' in el and 'root' in el['classes']), None)
            
            if not root_node:
                print(f"[!] No root node found for {chain}")
                failed = True
                continue
                
            actual_id = root_node['data']['id']
            
            if actual_id == expected:
                print(f"[PASS] {chain}: {actual_id}")
            else:
                print(f"[FAIL] {chain}: Expected {expected}, got {actual_id}")
                failed = True
                
        except Exception as e:
            print(f"[ERROR] {chain}: {e}")
            failed = True

    if failed:
        sys.exit(1)
    else:
        print("[SUCCESS] All case sensitivity tests passed!")

if __name__ == "__main__":
    test_case_sensitivity()
