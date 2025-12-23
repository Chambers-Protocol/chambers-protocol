import os
import sys
import json
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
from mcp.server.fastmcp import FastMCP

# Import the Thermo Kernel
from thermo_kernel import ThermoInnovationEngine

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
mcp = FastMCP("Chambers Thermoelectric Node")
thermo_engine = ThermoInnovationEngine()

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ THERMO NODE: Connected to Central Ledger")
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
            "p_operation": "THERMO_AUDIT",
            "p_fidelity_tax_usd": 0.01,
            "p_request_id": None, 
            # ANALYTICS TAG:
            "p_metadata": {"node": "thermo_innovation_v1"}
        }).execute()
        return response.data
    except Exception as e:
        print(f"Billing Error: {e}")
        return False

# --- THE TOOL ---
@mcp.tool()
def audit_thermo_viability(
    temperature_gradient_efficiency: float = 0.8,
    heat_flux_stability: float = 0.9,
    energy_source_density: float = 0.85,
    figure_of_merit_zt: float = 0.7,
    material_thermal_stability: float = 0.9,
    electrical_conductivity_opt: float = 0.8,
    fabrication_yield: float = 0.8,
    thin_film_deposition_efficiency: float = 0.75,
    cost_per_watt_viability: float = 0.6,
    waste_heat_capture_rate: float = 0.5,
    material_recyclability: float = 0.7,
    grid_integration_readiness: float = 0.8
) -> str:
    """
    Analyzes Thermoelectric Innovation Viability across Physics, Materials, Mfg, and Waste.
    Inputs: 0.0 to 1.0. 
    High ZT and Manufacturing Scalability are critical.
    """
    
    # 1. PAY TAX
    if not authorize_transaction(cost=10):
        return "⛔ ACCESS DENIED: Insufficient Credits."

    # 2. EXECUTE LOGIC
    inputs = {
        "temperature_gradient_efficiency": temperature_gradient_efficiency,
        "heat_flux_stability": heat_flux_stability,
        "energy_source_density": energy_source_density,
        "figure_of_merit_zt": figure_of_merit_zt,
        "material_thermal_stability": material_thermal_stability,
        "electrical_conductivity_opt": electrical_conductivity_opt,
        "fabrication_yield": fabrication_yield,
        "thin_film_deposition_efficiency": thin_film_deposition_efficiency,
        "cost_per_watt_viability": cost_per_watt_viability,
        "waste_heat_capture_rate": waste_heat_capture_rate,
        "material_recyclability": material_recyclability,
        "grid_integration_readiness": grid_integration_readiness
    }
    
    result = thermo_engine.compute_thermo_fidelity(inputs)
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    mcp.run()