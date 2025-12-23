import os
import sys
import json
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
from mcp.server.fastmcp import FastMCP

# Import Kernel
from research_kernel import ResearchInnovationEngine

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
mcp = FastMCP("Chambers Research Node")
research_engine = ResearchInnovationEngine()

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ RESEARCH NODE: Connected to Central Ledger")
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
            "p_operation": "RESEARCH_AUDIT",
            "p_fidelity_tax_usd": 0.01,
            "p_request_id": None, 
            # ANALYTICS TAG:
            "p_metadata": {"node": "research_hpqai_v1"}
        }).execute()
        return response.data
    except Exception as e:
        print(f"Billing Error: {e}")
        return False

# --- THE TOOL ---
@mcp.tool()
def audit_innovation_potential(
    quantum_computing_fidelity: float = 0.5,
    ai_model_accuracy: float = 0.8,
    hpc_throughput: float = 0.95,
    scientific_research_data: float = 0.7,
    engineering_data: float = 0.7,
    medical_research_data: float = 0.7,
    manufacturing_data: float = 0.7
) -> str:
    """
    Analyzes Research & Innovation Potential using HPQAI mechanics.
    Inputs: 0.0 to 1.0.
    Combines Quantum, AI, and HPC fidelity to predict breakthrough probability.
    """
    
    # 1. PAY TAX
    if not authorize_transaction(cost=10):
        return "⛔ ACCESS DENIED: Insufficient Credits."

    # 2. EXECUTE LOGIC
    inputs = {
        "quantum_computing_fidelity": quantum_computing_fidelity,
        "ai_model_accuracy": ai_model_accuracy,
        "hpc_throughput": hpc_throughput,
        "scientific_research_data": scientific_research_data,
        "engineering_data": engineering_data,
        "medical_research_data": medical_research_data,
        "manufacturing_data": manufacturing_data
    }
    
    result = research_engine.compute_innovation_potential(inputs)
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    mcp.run()