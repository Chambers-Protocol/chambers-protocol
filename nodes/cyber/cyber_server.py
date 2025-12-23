import os
import sys
import json
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
from mcp.server.fastmcp import FastMCP

# Import the Cyber Kernel
from cyber_kernel import CyberSecEngine

# --- CONFIG ---
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent.parent.parent

env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("CENTRAL_LEDGER_URL")
SUPABASE_KEY = os.getenv("CENTRAL_LEDGER_SECRET")
NODE_API_KEY = os.getenv("CHAMBERS_API_KEY")

# --- INITIALIZE ---
mcp = FastMCP("Chambers Cybersecurity Node")
cyber_engine = CyberSecEngine()

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ CYBER NODE: Connected to Central Ledger")
except Exception as e:
    print(f"❌ FATAL: Ledger Connection Failed - {e}")
    sys.exit(1)

# --- BILLING ---
def authorize_transaction(cost=10):
    if not NODE_API_KEY: return False
    hashed_key = hashlib.sha256(NODE_API_KEY.encode()).hexdigest()
    
    try:
        response = supabase.rpc("consume_credits", {
            "p_api_key_hash": hashed_key,
            "p_cost": cost,
            "p_operation": "CYBER_AUDIT",
            "p_fidelity_tax_usd": 0.01,
            "p_request_id": None, 
            # ANALYTICS TAG:
            "p_metadata": {"node": "cyber_security_v1"}
        }).execute()
        return response.data
    except Exception as e:
        print(f"Billing Error: {e}")
        return False

# --- THE TOOL ---
@mcp.tool()
def audit_cyber_posture(
    mfa_coverage: float = 1.0,
    least_privilege_enforcement: float = 0.9,
    privileged_access_mgmt: float = 0.8,
    siem_coverage: float = 0.8,
    endpoint_detection: float = 0.9,
    incident_response_readiness: float = 0.7,
    encryption_at_rest: float = 1.0,
    data_loss_prevention: float = 0.7,
    immutable_backups: float = 0.9,
    phishing_resilience: float = 0.6,
    security_awareness_training: float = 0.8,
    policy_enforcement: float = 0.9,
    audit_frequency: float = 0.8,
    vendor_risk_mgmt: float = 0.7
) -> str:
    """
    Analyzes Cybersecurity Posture via the Multiplicative Defense Chain.
    Inputs: 0.0 to 1.0. 
    Warning: Low scores in 'Human Factor' or 'IAM' effectively zero out the score.
    """
    
    # 1. PAY TAX
    if not authorize_transaction(cost=10):
        return "⛔ ACCESS DENIED: Insufficient Credits."

    # 2. EXECUTE LOGIC
    inputs = {
        "mfa_coverage": mfa_coverage,
        "least_privilege_enforcement": least_privilege_enforcement,
        "privileged_access_mgmt": privileged_access_mgmt,
        "siem_coverage": siem_coverage,
        "endpoint_detection": endpoint_detection,
        "incident_response_readiness": incident_response_readiness,
        "encryption_at_rest": encryption_at_rest,
        "data_loss_prevention": data_loss_prevention,
        "immutable_backups": immutable_backups,
        "phishing_resilience": phishing_resilience,
        "security_awareness_training": security_awareness_training,
        "policy_enforcement": policy_enforcement,
        "audit_frequency": audit_frequency,
        "vendor_risk_mgmt": vendor_risk_mgmt
    }
    
    result = cyber_engine.compute_security_posture(inputs)
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    mcp.run()