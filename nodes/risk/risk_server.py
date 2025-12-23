import os
import sys
import json
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
from mcp.server.fastmcp import FastMCP

# Import your Logic Kernel
from risk_kernel import RiskMechanicsEngine

# --- 1. CONFIGURATION & PATHS ---
# Determine if running as script or frozen .exe
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    # If running as script, go up two levels to find the root (chambers-protocol)
    BASE_DIR = Path(__file__).parent.parent.parent

# Load Secrets
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("CENTRAL_LEDGER_URL")
SUPABASE_KEY = os.getenv("CENTRAL_LEDGER_SECRET")
NODE_API_KEY = os.getenv("CHAMBERS_API_KEY")

# --- 2. INITIALIZE SERVER & LEDGER ---
mcp = FastMCP("Chambers Risk Node")
risk_engine = RiskMechanicsEngine()

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ RISK NODE: Connected to Central Ledger")
except Exception as e:
    print(f"❌ FATAL: Ledger Connection Failed - {e}")
    sys.exit(1)

# --- 3. THE PAYMENT GATE (Shared Logic) ---
def authorize_transaction(cost=10):
    """
    Deducts credits from the Central Ledger. 
    Returns True if approved, False if denied.
    """
    if not NODE_API_KEY:
        return False
        
    hashed_key = hashlib.sha256(NODE_API_KEY.encode()).hexdigest()
    
    try:
        response = supabase.rpc("consume_credits", {
            "p_api_key_hash": hashed_key,
            "p_cost": cost,
            "p_operation": "RISK_AUDIT",
            "p_fidelity_tax_usd": 0.01,
            "p_request_id": None, 
            "p_metadata": {"node": "risk_mechanics_v1"}
        }).execute()
        
        return response.data  # True/False
    except Exception as e:
        print(f"Billing Error: {e}")
        return False

# --- 4. THE TOOL ---
@mcp.tool()
def audit_risk_architecture(
    philosophy_alignment: float = 0.9,
    strategy_implementation: float = 0.9,
    model_robustness: float = 0.85,
    data_integrity: float = 0.9,
    liquidity_depth: float = 0.8,
    execution_speed: float = 0.95,
    stress_testing_rigor: float = 0.7,
    portfolio_optimization: float = 0.85,
    regulatory_adherence: float = 1.0,
    operational_resilience: float = 0.9
) -> str:
    """
    Analyzes an organizational risk architecture using the Multiplicative Risk Chain.
    Inputs should be 0.0 to 1.0. 
    
    Returns a deterministic audit identifying the 'Critical Constraint Node'.
    """
    
    # 1. BILLING CHECK
    if not authorize_transaction(cost=10):
        return "⛔ ACCESS DENIED: Insufficient Credits or Invalid License."

    # 2. RUN LOGIC KERNEL
    inputs = {
        "philosophy_alignment": philosophy_alignment,
        "strategy_implementation": strategy_implementation,
        "model_robustness": model_robustness,
        "data_integrity": data_integrity,
        "liquidity_depth": liquidity_depth,
        "execution_speed": execution_speed,
        "stress_testing_rigor": stress_testing_rigor,
        "portfolio_optimization": portfolio_optimization,
        "regulatory_adherence": regulatory_adherence,
        "operational_resilience": operational_resilience
    }
    
    result = risk_engine.compute_risk_fidelity(inputs)
    
    # 3. RETURN JSON
    return json.dumps(result, indent=2)

# --- 5. EXECUTION ---
if __name__ == "__main__":
    mcp.run()