import os
import sys
import json
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
from mcp.server.fastmcp import FastMCP

# Import the Cloud Kernel
from cloud_kernel import CloudOpsEngine

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
mcp = FastMCP("Chambers Cloud Ops Node")
cloud_engine = CloudOpsEngine()

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ CLOUD NODE: Connected to Central Ledger")
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
            "p_operation": "CLOUD_AUDIT",
            "p_fidelity_tax_usd": 0.01,
            "p_request_id": None, 
            # ANALYTICS TAG:
            "p_metadata": {"node": "cloud_ops_v1"}
        }).execute()
        return response.data
    except Exception as e:
        print(f"Billing Error: {e}")
        return False

# --- THE TOOL ---
@mcp.tool()
def audit_cloud_operations(
    architecture_soundness: float = 0.9,
    network_connectivity: float = 0.95,
    multicloud_portability: float = 0.8,
    iam_security_posture: float = 1.0,
    governance_compliance: float = 1.0,
    automation_level: float = 0.7,
    cost_allocation_tagging: float = 0.6,
    resource_utilization_rate: float = 0.75,
    budget_forecasting_accuracy: float = 0.8,
    sre_reliability_index: float = 0.9,
    deployment_velocity: float = 0.85,
    disaster_recovery_readiness: float = 0.9
) -> str:
    """
    Analyzes Cloud Operations Maturity across Infrastructure, Hygiene, FinOps, and Resilience.
    Inputs: 0.0 to 1.0.
    """
    
    # 1. PAY TAX
    if not authorize_transaction(cost=10):
        return "⛔ ACCESS DENIED: Insufficient Credits."

    # 2. EXECUTE LOGIC
    inputs = {
        "architecture_soundness": architecture_soundness,
        "network_connectivity": network_connectivity,
        "multicloud_portability": multicloud_portability,
        "iam_security_posture": iam_security_posture,
        "governance_compliance": governance_compliance,
        "automation_level": automation_level,
        "cost_allocation_tagging": cost_allocation_tagging,
        "resource_utilization_rate": resource_utilization_rate,
        "budget_forecasting_accuracy": budget_forecasting_accuracy,
        "sre_reliability_index": sre_reliability_index,
        "deployment_velocity": deployment_velocity,
        "disaster_recovery_readiness": disaster_recovery_readiness
    }
    
    result = cloud_engine.compute_cloud_fidelity(inputs)
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    mcp.run()