import os
import sys
import json
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
from mcp.server.fastmcp import FastMCP

# Import the Oil Kernel
from oil_kernel import OilSingularityEngine

# --- CONFIG & SECRETS ---
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
mcp = FastMCP("Chambers Oil & Gas Node")
oil_engine = OilSingularityEngine()

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ OIL NODE: Connected to Central Ledger")
except Exception as e:
    print(f"❌ FATAL: Ledger Connection Failed - {e}")
    sys.exit(1)

# --- BILLING GATE ---
def authorize_transaction(cost=10):
    if not NODE_API_KEY: return False
    hashed_key = hashlib.sha256(NODE_API_KEY.encode()).hexdigest()
    
    try:
        response = supabase.rpc("consume_credits", {
            "p_api_key_hash": hashed_key,
            "p_cost": cost,
            "p_operation": "SINGULARITY_COMPUTE",
            "p_fidelity_tax_usd": 0.01,
            "p_request_id": None, 
            # HERE IS THE TAG FOR YOUR ANALYTICS:
            "p_metadata": {"node": "oil_gas_singularity_v1"}
        }).execute()
        return response.data
    except Exception as e:
        print(f"Billing Error: {e}")
        return False

# --- THE TOOL ---
@mcp.tool()
def compute_extraction_singularity(
    reservoir_simulation_accuracy: float = 0.9,
    seismic_clarity: float = 0.85,
    predictive_maintenance_ai: float = 0.8,
    geological_certainty: float = 0.7,
    drilling_technology_tier: float = 0.9,
    material_durability: float = 0.9,
    safety_protocols: float = 1.0,
    environmental_compliance: float = 1.0,
    process_automation: float = 0.8,
    global_demand_index: float = 0.9,
    opex_reduction_target: float = 0.8
) -> str:
    """
    Calculates the O&G Singularity Index based on computational, engineering, 
    and operational inputs (0.0 - 1.0).
    """
    
    # 1. PAY THE FIDELITY TAX
    if not authorize_transaction(cost=10):
        return "⛔ ACCESS DENIED: Insufficient Credits."

    # 2. RUN THE PHYSICS
    inputs = {
        "reservoir_simulation_accuracy": reservoir_simulation_accuracy,
        "seismic_clarity": seismic_clarity,
        "predictive_maintenance_ai": predictive_maintenance_ai,
        "geological_certainty": geological_certainty,
        "drilling_technology_tier": drilling_technology_tier,
        "material_durability": material_durability,
        "safety_protocols": safety_protocols,
        "environmental_compliance": environmental_compliance,
        "process_automation": process_automation,
        "global_demand_index": global_demand_index,
        "opex_reduction_target": opex_reduction_target
    }
    
    result = oil_engine.compute_singularity_index(inputs)
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    mcp.run()