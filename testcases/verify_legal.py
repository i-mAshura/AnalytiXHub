
import os
import sys
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.reports.legal_report import LegalReportGenerator

# Mock Data (Solana-style mixed case)
ROOT_ADDR = "H8smjscqxfkiftcfdr3dumlpwcrbm61lgfj8n4dk3w"
COUNTERPARTY = "Gjrs4fwhtemz5ze9x3fnvj8tmwitkth21yxdrpqn7np"

mock_summary = {
    "total_transactions": 150,
    "total_received": 100.5,
    "total_sent": 50.2,
    "net_flow": 50.3,
    "risk_score": 85,
    "confidence_score": 90,
    "entity_type": "Unknown",
    "patterns_detected": ["rapid_succession", "high_frequency"],
    "top_victims": [(COUNTERPARTY, 2.0)],
    "top_suspects": [(COUNTERPARTY, 1.5)],
    "cash_out_points": ["2.0 ETH -> Exchange"],
    "inbound_count": 100,
    "outbound_count": 50
}

mock_analysis = {
    "narrative": "This is a test narrative for the legal report."
}

def verify_legal():
    print("Verifying Legal Report Generator...")
    
    gen = LegalReportGenerator("Test Case 123", "Officer Smith", "Cyber Unit")
    
    # 1. FIR Report
    print("1. Testing FIR Report...")
    res = gen.create_fir_report(mock_summary, mock_analysis, ROOT_ADDR, "test_fir.pdf")
    if res and os.path.exists(res):
        print("   PASS: FIR Report generated.")
    else:
        print("   FAIL: FIR Report generation failed.")
        
    # 2. Evidence Report
    print("2. Testing Evidence Report...")
    res = gen.create_evidence_report(mock_summary, ["rapid_succession"], "test_evidence.pdf")
    if res and os.path.exists(res):
        print("   PASS: Evidence Report generated.")
    else:
        print("   FAIL: Evidence Report generation failed.")

if __name__ == "__main__":
    verify_legal()
