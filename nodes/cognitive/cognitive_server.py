import os
import sys
import json
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
from mcp.server.fastmcp import FastMCP

# Import Kernel
from cognitive_kernel import CognitiveArchEngine

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
mcp = FastMCP("Chambers Cognitive Framework Node")
cognitive_engine = CognitiveArchEngine()

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ COGNITIVE NODE: Connected to Central Ledger")
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
            "p_operation": "COGNITIVE_AUDIT",
            "p_fidelity_tax_usd": 0.01,
            "p_request_id": None, 
            "p_metadata": {"node": "cognitive_framework_v1"}
        }).execute()
        return response.data
    except Exception as e:
        print(f"Billing Error: {e}")
        return False

# --- THE TOOL ---
@mcp.tool()
def audit_cognitive_architecture(
    neural_synapse_fire_rate: float = 0.9,
    processing_speed_ms: float = 0.85,
    sensory_input_volume: float = 0.8,
    orientation_ie: float = 0.5, # 0.0=Introvert, 1.0=Extrovert
    orientation_ns: float = 0.5, # 0.0=Sensing, 1.0=Intuitive
    orientation_tf: float = 0.5, # 0.0=Feeling, 1.0=Thinking
    orientation_jp: float = 0.5, # 0.0=Perceiving, 1.0=Judging
    early_influence_coherence: float = 0.7,
    mentorship_quality: float = 0.8,
    years_of_experience_index: float = 0.6,
    intrinsic_motivation: float = 0.9,
    skill_competence: float = 0.8,
    situational_constraints: float = 0.2
) -> str:
    """
    Analyzes Psychological Framework and Cognitive Velocity.
    Inputs: 0.0 to 1.0. 
    Determines MBTI-style type and processing efficiency.
    """
    
    # 1. PAY TAX
    if not authorize_transaction(cost=10):
        return "⛔ ACCESS DENIED: Insufficient Credits."

    # 2. EXECUTE LOGIC
    inputs = {
        "neural_synapse_fire_rate": neural_synapse_fire_rate,
        "processing_speed_ms": processing_speed_ms,
        "sensory_input_volume": sensory_input_volume,
        "orientation_ie": orientation_ie,
        "orientation_ns": orientation_ns,
        "orientation_tf": orientation_tf,
        "orientation_jp": orientation_jp,
        "early_influence_coherence": early_influence_coherence,
        "mentorship_quality": mentorship_quality,
        "years_of_experience_index": years_of_experience_index,
        "intrinsic_motivation": intrinsic_motivation,
        "skill_competence": skill_competence,
        "situational_constraints": situational_constraints
    }
    
    result = cognitive_engine.compute_cognitive_physics(inputs)
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    mcp.run()