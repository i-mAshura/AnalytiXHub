"""
Multi-Chain Blockchain Data Fetcher
Supports multiple chains via official and public APIs:
  - EVM Chains: Ethereum, Polygon, Arbitrum, Optimism, BSC (Etherscan v2 / BlockScout)
  - Bitcoin: Mempool.space (Free)
  - Solana: Solscan Public API v2 (Official)
  - Tron: TronGrid / TronScan (Official)
  - XRP: XRPL Public Nodes
"""
import requests
import time
import random
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
SOLANA_API_KEY = os.getenv('SOLANA_API_KEY', "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE3NzA3MTg3MzU5ODAsImVtYWlsIjoia29sbHVydXNhaWFiaGlyYW01MTNAZ21haWwuY29tIiwiYWN0aW9uIjoidG9rZW4tYXBpIiwiYXBpVmVyc2lvbiI6InYyIiwiaWF0IjoxNzcwNzE4NzM1fQ.SGdL7FJRYiMhC5YnSky-6UXCa4NLOgkoWSvhD2AvRDg")
TRON_API_KEY = os.getenv('TRON_API_KEY', "72ac1d93-4497-4664-a844-f730b2b5e606")

# ==================== BLOCKSCOUT (Free EVM API) ====================

class BlockScoutFetcher:
    """Fetch transactions via BlockScout - FREE for all EVM chains"""
    
    BLOCKSCOUT_URLS = {
        'ethereum': 'https://eth.blockscout.com/api/v2',
        'polygon': 'https://polygon.blockscout.com/api/v2',
        'arbitrum': 'https://arbitrum.blockscout.com/api/v2',
        'optimism': 'https://optimism.blockscout.com/api/v2',
    }
    
    @staticmethod
    def fetch_transactions(chain: str, address: str) -> Tuple[List[Dict], Dict]:
        """Fetch via BlockScout (100% FREE, no API key needed)"""
        chain = chain.lower()
        if chain not in BlockScoutFetcher.BLOCKSCOUT_URLS:
            return [], {'normal': 0, 'internal': 0, 'token': 0}
        
        base_url = BlockScoutFetcher.BLOCKSCOUT_URLS[chain]
        transactions = []
        counts = {'normal': 0, 'internal': 0, 'token': 0}
        
        try:
            tx_url = f"{base_url}/addresses/{address}/transactions"
            tx_response = requests.get(tx_url, timeout=15)
            
            if tx_response.status_code == 200:
                tx_data = tx_response.json()
                if 'items' in tx_data:
                    for tx in tx_data['items'][:50]:
                        transactions.append({
                            'hash': tx.get('hash'),
                            'from': tx.get('from', {}).get('hash') if isinstance(tx.get('from'), dict) else tx.get('from'),
                            'to': tx.get('to', {}).get('hash') if isinstance(tx.get('to'), dict) else tx.get('to'),
                            'value': float(tx.get('value', 0)) if tx.get('value') else 0,
                            'timestamp': tx.get('timestamp') or datetime.now().isoformat(),
                            'block': tx.get('block', 0),
                            'chain': chain
                        })
                counts['normal'] = len(transactions)
                print(f"✅ {chain.upper()} (BlockScout): {counts['normal']} transactions")
            
            return transactions, counts
        
        except Exception as e:
            print(f"❌ BlockScout {chain} error: {e}")
            return [], counts

# ==================== ETHERSCAN v2 API (All EVM Chains) ====================

class EtherscanMultiChainFetcher:
    """
    Fetch transactions from EVM chains using Etherscan v2 API
    Uses SINGLE endpoint: https://api.etherscan.io/v2/api with chainid parameter
    """
    
    V2_ENDPOINT = 'https://api.etherscan.io/v2/api'
    
    CHAIN_CONFIGS = {
        'ethereum': {'chainid': 1, 'name': 'Ethereum'},
        'bsc': {'chainid': 56, 'name': 'Binance Smart Chain'},
        'polygon': {'chainid': 137, 'name': 'Polygon'},
        'optimism': {'chainid': 10, 'name': 'Optimism'},
        'arbitrum': {'chainid': 42161, 'name': 'Arbitrum One'},
        'avalanche': {'chainid': 43114, 'name': 'Avalanche'},
        'fantom': {'chainid': 250, 'name': 'Fantom'},
    }
    
    @staticmethod
    def fetch_transactions(chain: str, address: str, include_internal: bool = True, 
                          include_token: bool = True) -> Tuple[List[Dict], Dict]:
        
        chain = chain.lower()
        if chain not in EtherscanMultiChainFetcher.CHAIN_CONFIGS:
            # Try BlockScout fallback immediately if chain not supported here but supported there
             return BlockScoutFetcher.fetch_transactions(chain, address)
        
        config = EtherscanMultiChainFetcher.CHAIN_CONFIGS[chain]
        transactions = []
        counts = {'normal': 0, 'internal': 0, 'token': 0}
        
        # Fallback to BlockScout if no key
        if not ETHERSCAN_API_KEY:
            print(f"⚠️  No Etherscan API key, using BlockScout for {config['name']}...")
            return BlockScoutFetcher.fetch_transactions(chain, address)
        
        try:
            print(f"[+] Fetching {config['name']} transactions via Etherscan v2 API...")
            
            # Normal transactions
            normal_txs = EtherscanMultiChainFetcher._fetch_page(chain, address, 'txlist')
            transactions.extend(normal_txs)
            counts['normal'] = len(normal_txs)
            
            # Internal transactions
            if include_internal:
                internal_txs = EtherscanMultiChainFetcher._fetch_page(chain, address, 'txlistinternal')
                transactions.extend(internal_txs)
                counts['internal'] = len(internal_txs)
            
            # Token transfers
            if include_token:
                token_txs = EtherscanMultiChainFetcher._fetch_page(chain, address, 'tokentx')
                transactions.extend(token_txs)
                counts['token'] = len(token_txs)
            
            total = counts['normal'] + counts['internal'] + counts['token']
            print(f"✅ {config['name']}: {counts['normal']} normal, {counts['internal']} internal, {counts['token']} token ({total} total)")
            return transactions, counts
        
        except Exception as e:
            print(f"❌ {config['name']} fetch error: {e}")
            print(f"   Falling back to BlockScout...")
            return BlockScoutFetcher.fetch_transactions(chain, address)
    
    @staticmethod
    def _fetch_page(chain: str, address: str, action: str, page: int = 1, offset: int = 50) -> List[Dict]:
        config = EtherscanMultiChainFetcher.CHAIN_CONFIGS[chain]
        params = {
            'chainid': config['chainid'],
            'module': 'account',
            'action': action,
            'address': address,
            'page': page,
            'offset': offset,
            'sort': 'desc',
            'apikey': ETHERSCAN_API_KEY
        }
        
        try:
            response = requests.get(EtherscanMultiChainFetcher.V2_ENDPOINT, params=params, timeout=10)
            data = response.json()
            
            if data.get('status') == '1' and data.get('result'):
                # Normalize results
                results = []
                for tx in data['result']:
                    tx['chain'] = chain
                    if 'timeStamp' in tx: # Normalize timestamp format
                        try:
                            tx['timestamp'] = datetime.fromtimestamp(int(tx['timeStamp'])).strftime('%Y-%m-%d %H:%M:%S')
                        except:
                            pass
                    results.append(tx)
                return results
            return []
        except:
            return []


# ==================== BITCOIN (Mempool.space) ====================

class MempoolFetcher:
    """Fetch Bitcoin transactions via Mempool.space (Free, No Key)"""
    
    BASE_URL = "https://mempool.space/api"
    
    @staticmethod
    def fetch_transactions(address: str) -> Tuple[List[Dict], Dict]:
        transactions = []
        counts = {'normal': 0}
        
        try:
            print(f"[+] Fetching Bitcoin data from Mempool.space for {address[:8]}...")
            url = f"{MempoolFetcher.BASE_URL}/address/{address}/txs"
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                tx_data = response.json()
                
                for tx in tx_data:
                    # Parse Bitcoin transaction
                    tx_hash = tx.get('txid')
                    status = tx.get('status', {})
                    block_time = status.get('block_time', int(time.time()))
                    
                    # Calculate value flow relative to this address
                    value = 0
                    flow_type = 'unknown'
                    
                    # Check inputs (sending)
                    inputs_val = sum(inp.get('prevout', {}).get('value', 0) for inp in tx.get('vin', []) 
                                   if inp.get('prevout', {}).get('scriptpubkey_address') == address)
                    
                    # Check outputs (receiving)
                    outputs_val = sum(out.get('value', 0) for out in tx.get('vout', []) 
                                    if out.get('scriptpubkey_address') == address)
                    
                    if inputs_val > 0:
                        value = (inputs_val - outputs_val) / 1e8 # Sent amount (Satoshis -> BTC)
                        flow_type = 'out'
                        counterparty = "Multiple Inputs" # Simplified
                    else:
                        value = outputs_val / 1e8 # Received amount
                        flow_type = 'in'
                        counterparty = "Multiple Outputs"
                    
                    transactions.append({
                        'hash': tx_hash,
                        'timestamp': datetime.fromtimestamp(block_time).strftime('%Y-%m-%d %H:%M:%S'),
                        'value': abs(value),
                        'from': address if flow_type == 'out' else 'Incoming',
                        'to': 'Outgoing' if flow_type == 'out' else address,
                        'chain': 'bitcoin',
                        'flow': flow_type
                    })
                
                counts['normal'] = len(transactions)
                print(f"✅ Bitcoin (Mempool): {counts['normal']} transactions")
            else:
                print(f"❌ Mempool API error: {response.status_code}")
                
            return transactions, counts
            
        except Exception as e:
            print(f"❌ Bitcoin fetch error: {e}")
            return [], counts


# ==================== SOLANA (Solscan v2) ====================

class SolanaFetcher:
    """Fetch Solana transactions via Solscan API v2"""
    
    BASE_URL = "https://pro-api.solscan.io/v2.0" # Using Pro/Public v2 endpoint
    
    @staticmethod
    def fetch_transactions(address: str) -> Tuple[List[Dict], Dict]:
        transactions = []
        counts = {'normal': 0}
        
        headers = {
            "token": SOLANA_API_KEY
        }
        
        try:
            print(f"[+] Fetching Solana data from Solscan for {address[:8]}...")
            
            # Use account/transactions endpoint
            url = f"{SolanaFetcher.BASE_URL}/account/transfer"
            params = {'address': address, 'limit': 40}
            
            response = requests.get(url, headers=headers, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('data'):
                    for tx in data['data']:
                        # Parse Solscan transfer data
                        amount = float(tx.get('amount', 0)) / (10 ** tx.get('decimals', 9))
                        
                        transactions.append({
                            'hash': tx.get('trans_id'),
                            'timestamp': datetime.fromtimestamp(tx.get('block_time', time.time())).strftime('%Y-%m-%d %H:%M:%S'),
                            'value': amount,
                            'from': tx.get('source_owner'),
                            'to': tx.get('dest_owner'),
                            'chain': 'solana',
                            'token': tx.get('token_address', 'SOL')
                        })
                    
                    counts['normal'] = len(transactions)
                    print(f"✅ Solana (Solscan): {counts['normal']} transactions")
                else:
                    print(f"⚠️ Solscan returned no success: {data}")
            else:
                print(f"❌ Solscan API error: {response.status_code} - {response.text}")
                
            return transactions, counts
            
        except Exception as e:
            print(f"❌ Solana fetch error: {e}")
            return [], counts


# ==================== TRON (TronGrid / TronScan) ====================

class TronFetcher:
    """Fetch Tron transactions via TronGrid"""
    
    BASE_URL = "https://api.trongrid.io"
    
    @staticmethod
    def fetch_transactions(address: str) -> Tuple[List[Dict], Dict]:
        transactions = []
        counts = {'normal': 0}
        
        headers = {
            "TRON-PRO-API-KEY": TRON_API_KEY
        }
        
        try:
            print(f"[+] Fetching Tron data for {address[:8]}...")
            
            # TronGrid /v1/accounts/{address}/transactions
            url = f"{TronFetcher.BASE_URL}/v1/accounts/{address}/transactions"
            params = {'limit': 50}
            
            response = requests.get(url, headers=headers, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('data'):
                    for tx in data['data']:
                        # Parse Tron Data
                        raw_data = tx.get('raw_data', {}).get('contract', [])[0]
                        params = raw_data.get('parameter', {}).get('value', {})
                        
                        amount = float(params.get('amount', 0)) / 1e6 # Sun to TRX
                        if amount == 0 and 'asset_name' in params:
                             # TRC10 token maybe?
                             pass
                             
                        timestamp = tx.get('block_timestamp', 0) / 1000
                        
                        transactions.append({
                            'hash': tx.get('txID'),
                            'timestamp': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                            'value': amount,
                            'from': params.get('owner_address'), # Usually hex
                            'to': params.get('to_address'),
                            'chain': 'tron',
                            'type': raw_data.get('type')
                        })
                        
                    counts['normal'] = len(transactions)
                    print(f"✅ Tron (TronGrid): {counts['normal']} transactions")
            else:
                print(f"❌ TronGrid API error: {response.status_code}")
                
            return transactions, counts
            
        except Exception as e:
            print(f"❌ Tron fetch error: {e}")
            return [], counts


# ==================== XRP LEDGER ====================

class XRPLFetcher:
    """Fetch XRP transactions via XRPL public nodes"""
    
    NODES = [
        'https://xrplcluster.com',
        'https://s1.ripple.com:51234',
    ]
    
    @staticmethod
    def fetch_transactions(address: str, limit: int = 50) -> Tuple[List[Dict], Dict]:
        transactions = []
        counts = {'normal': 0}
        
        for node_url in XRPLFetcher.NODES:
            try:
                payload = {
                    "method": "account_tx",
                    "params": [{
                        "account": address,
                        "limit": limit
                    }]
                }
                
                response = requests.post(node_url, json=payload, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if 'result' in data and 'transactions' in data['result']:
                        for item in data['result']['transactions']:
                            tx = item.get('tx', {})
                            transactions.append({
                                'hash': tx.get('hash'),
                                'timestamp': datetime.fromtimestamp(946684800 + tx.get('date', 0)).strftime('%Y-%m-%d %H:%M:%S'), # Ripple Epoch
                                'value': float(tx.get('Amount', 0)) / 1e6 if isinstance(tx.get('Amount'), str) else 0,
                                'from': tx.get('Account'),
                                'to': tx.get('Destination'),
                                'chain': 'xrp'
                            })
                        counts['normal'] = len(transactions)
                        print(f"✅ XRP: {counts['normal']} transactions")
                        return transactions, counts
            except:
                continue
                
        return [], counts


# ==================== UNIFIED INTERFACE ====================

class MultiChainFetcher:
    """Unified interface for all blockchain chains"""
    
    @staticmethod
    def fetch_by_chain(chain: str, address: str, **kwargs) -> Tuple[List[Dict], Dict]:
        """Universal fetch method for any chain"""
        
        chain = chain.lower()
        
        # EVM Chains
        if chain in ['ethereum', 'ethereum', 'eth']:
            return EtherscanMultiChainFetcher.fetch_transactions('ethereum', address, **kwargs)
        elif chain in ['polygon', 'matic']:
            return EtherscanMultiChainFetcher.fetch_transactions('polygon', address, **kwargs)
        elif chain in ['arbitrum', 'arb']:
            return EtherscanMultiChainFetcher.fetch_transactions('arbitrum', address, **kwargs)
        elif chain in ['optimism', 'op']:
            return EtherscanMultiChainFetcher.fetch_transactions('optimism', address, **kwargs)
        elif chain in ['bsc', 'binance', 'bnb']:
            return EtherscanMultiChainFetcher.fetch_transactions('bsc', address, **kwargs)
            
        # Non-EVM Chains (Real Implementations)
        elif chain in ['bitcoin', 'btc']:
            return MempoolFetcher.fetch_transactions(address)
        elif chain in ['solana', 'sol']:
            return SolanaFetcher.fetch_transactions(address)
        elif chain in ['tron', 'trx']:
            return TronFetcher.fetch_transactions(address)
        elif chain in ['xrp', 'ripple']:
            return XRPLFetcher.fetch_transactions(address)
            
        else:
            print(f"⚠️ Unsupported chain '{chain}', defaulting to empty")
            return [], {}
    
    @staticmethod
    def get_explorer_url(chain: str, address: str) -> str:
        explorers = {
            'ethereum': f'https://etherscan.io/address/{address}',
            'polygon': f'https://polygonscan.com/address/{address}',
            'bitcoin': f'https://mempool.space/address/{address}',
            'solana': f'https://solscan.io/account/{address}',
            'tron': f'https://tronscan.org/#/address/{address}',
            'xrp': f'https://xrpscan.com/account/{address}',
        }
        return explorers.get(chain, '#')

if __name__ == '__main__':
    print("Test run...")
