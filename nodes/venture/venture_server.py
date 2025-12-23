import os
import sys
import json
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
from mcp.server.fastmcp import FastMCP

# Import Kernel
from venture_kernel import VentureArchEngine

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
mcp = FastMCP("Chambers Venture Architecture Node")
venture_engine = VentureArchEngine()

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ VENTURE NODE: Connected to Central Ledger")
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
            "p_operation": "VENTURE_AUDIT",
            "p_fidelity_tax_usd": 0.01,
            "p_request_id": None, 
            # ANALYTICS TAG:
            "p_metadata": {"node": "venture_architecture_v1"}
        }).execute()
        return response.data
    except Exception as e:
        print(f"Billing Error: {e}")
        return False

# --- THE TOOL ---
@mcp.tool()
def audit_venture_viability(
    competitive_landscape_clarity: float = 0.8,
    existing_assets_leverage: float = 0.7,
    product_market_fit: float = 0.6,
    backlog_prioritization: float = 0.8,
    business_plan_solidity: float = 0.9,
    speed_to_market: float = 0.7,
    marketing_strategy_efficacy: float = 0.7,
    sales_pipeline_velocity: float = 0.6,
    customer_retention_rate: float = 0.8,
    revenue_per_employee_efficiency: float = 0.5,
    competitive_win_rate: float = 0.5,
    tam_accessibility: float = 0.8
) -> str:
    """
    Analyzes a Venture's probability of success based on Foundation, Execution, and Growth mechanics.
    Inputs: 0.0 to 1.0.
    """
    
    # 1. PAY TAX
    if not authorize_transaction(cost=10):
        return "⛔ ACCESS DENIED: Insufficient Credits."

    # 2. EXECUTE LOGIC
    inputs = {
        "competitive_landscape_clarity": competitive_landscape_clarity,
        "existing_assets_leverage": existing_assets_leverage,
        "product_market_fit": product_market_fit,
        "backlog_prioritization": backlog_prioritization,
        "business_plan_solidity": business_plan_solidity,
        "speed_to_market": speed_to_market,
        "marketing_strategy_efficacy": marketing_strategy_efficacy,
        "sales_pipeline_velocity": sales_pipeline_velocity,
        "customer_retention_rate": customer_retention_rate,
        "revenue_per_employee_efficiency": revenue_per_employee_efficiency,
        "competitive_win_rate": competitive_win_rate,
        "tam_accessibility": tam_accessibility
    }
    
    result = venture_engine.compute_venture_valuation(inputs)
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    mcp.run()