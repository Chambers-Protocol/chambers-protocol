import os
import sys
import json
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
from mcp.server.fastmcp import FastMCP

# Import Kernel
from semi_kernel import SemiconductorEngine

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
mcp = FastMCP("Chambers Semiconductor Node")
semi_engine = SemiconductorEngine()

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ SEMI NODE: Connected to Central Ledger")
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
            "p_operation": "SEMI_AUDIT",
            "p_fidelity_tax_usd": 0.01,
            "p_request_id": None, 
            # ANALYTICS TAG:
            "p_metadata": {"node": "semiconductor_v1"}
        }).execute()
        return response.data
    except Exception as e:
        print(f"Billing Error: {e}")
        return False

# --- THE TOOL ---
@mcp.tool()
def audit_semiconductor_production(
    silicon_purity_level: float = 0.99,
    lithography_precision: float = 0.9,
    fabrication_yield_rate: float = 0.8,
    geopolitical_stability: float = 0.6,
    rare_earth_sourcing_secure: float = 0.7,
    equipment_uptime: float = 0.9,
    closed_loop_emissions: float = 0.6,
    renewable_energy_mix: float = 0.5,
    material_circularity: float = 0.4,
    metamaterial_integration: float = 0.2,
    ai_material_discovery: float = 0.8
) -> str:
    """
    Analyzes Semiconductor Production Viability & Sustainability.
    Inputs: 0.0 to 1.0.
    Balances Supply Chain Risks against Green Innovation.
    """
    
    # 1. PAY TAX
    if not authorize_transaction(cost=10):
        return "⛔ ACCESS DENIED: Insufficient Credits."

    # 2. EXECUTE LOGIC
    inputs = {
        "silicon_purity_level": silicon_purity_level,
        "lithography_precision": lithography_precision,
        "fabrication_yield_rate": fabrication_yield_rate,
        "geopolitical_stability": geopolitical_stability,
        "rare_earth_sourcing_secure": rare_earth_sourcing_secure,
        "equipment_uptime": equipment_uptime,
        "closed_loop_emissions": closed_loop_emissions,
        "renewable_energy_mix": renewable_energy_mix,
        "material_circularity": material_circularity,
        "metamaterial_integration": metamaterial_integration,
        "ai_material_discovery": ai_material_discovery
    }
    
    result = semi_engine.compute_chip_viability(inputs)
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    mcp.run()