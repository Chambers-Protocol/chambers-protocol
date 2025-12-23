import os
import sys
import json
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
from mcp.server.fastmcp import FastMCP

# Import Kernel
from product_kernel import ProductEngine

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
mcp = FastMCP("Chambers Product Strategy Node")
product_engine = ProductEngine()

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ PRODUCT NODE: Connected to Central Ledger")
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
            "p_operation": "PRODUCT_AUDIT",
            "p_fidelity_tax_usd": 0.01,
            "p_request_id": None, 
            # ANALYTICS TAG:
            "p_metadata": {"node": "product_strategy_v1"}
        }).execute()
        return response.data
    except Exception as e:
        print(f"Billing Error: {e}")
        return False

# --- THE TOOL ---
@mcp.tool()
def audit_product_strategy(
    competitive_landscape: float = 0.8,
    existing_assets_leverage: float = 0.7,
    product_market_fit: float = 0.6,
    backlog_prioritization: float = 0.8,
    buy_build_partner_decision: float = 0.9,
    business_plan_validity: float = 0.8,
    target_market_clarity: float = 0.7,
    brand_awareness: float = 0.6,
    outreach_tactics: float = 0.7,
    speed_to_market: float = 0.7,
    operational_alignment: float = 0.8
) -> str:
    """
    Analyzes Product Viability (Strategy + Management + Marketing).
    Inputs: 0.0 to 1.0.
    Calculates the 'Sales Opportunity Pipeline' potential.
    """
    
    # 1. PAY TAX
    if not authorize_transaction(cost=10):
        return "⛔ ACCESS DENIED: Insufficient Credits."

    # 2. EXECUTE LOGIC
    inputs = {
        "competitive_landscape": competitive_landscape,
        "existing_assets_leverage": existing_assets_leverage,
        "product_market_fit": product_market_fit,
        "backlog_prioritization": backlog_prioritization,
        "buy_build_partner_decision": buy_build_partner_decision,
        "business_plan_validity": business_plan_validity,
        "target_market_clarity": target_market_clarity,
        "brand_awareness": brand_awareness,
        "outreach_tactics": outreach_tactics,
        "speed_to_market": speed_to_market,
        "operational_alignment": operational_alignment
    }
    
    result = product_engine.compute_product_viability(inputs)
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    mcp.run()