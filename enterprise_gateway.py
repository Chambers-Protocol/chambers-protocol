import sys
import json
import os
import hashlib
from pathlib import Path
from fastmcp import FastMCP
from dotenv import load_dotenv
from supabase import create_client

# ==============================================================================
# 1. CONFIGURATION & IDENTITY
# ==============================================================================
script_dir = Path(__file__).parent.absolute()
env_path = script_dir / '.env'
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("CHAMBERS_API_KEY")
LEDGER_URL = os.getenv("CENTRAL_LEDGER_URL")
LEDGER_KEY = os.getenv("CENTRAL_LEDGER_SECRET")

supabase = None
hashed_key = None
axiom_kernel = None
configuration_error = None

if not API_KEY:
    configuration_error = "CRITICAL: API Key missing."
    print(configuration_error, file=sys.stderr)
elif not LEDGER_URL:
    configuration_error = "CRITICAL: Supabase URL missing."
    print(configuration_error, file=sys.stderr)
else:
    hashed_key = hashlib.sha256(API_KEY.encode()).hexdigest()
    try:
        supabase = create_client(LEDGER_URL, LEDGER_KEY)
    except Exception as e:
        configuration_error = f"Bank Connection Failed: {e}"
        print(configuration_error, file=sys.stderr)

# ==============================================================================
# 2. IMPORT THE SOVEREIGN KERNEL (The Black Box)
# ==============================================================================
try:
    from axiom import TheAxiom
    
    # Initialize The Axiom (The Single Source of Truth)
    if API_KEY:
        axiom_kernel = TheAxiom(partner_api_key=API_KEY)

except ImportError:
    print("CRITICAL: 'the-axiom' package not found. Install v1.2.0+.", file=sys.stderr)

# ==============================================================================
# 3. THE TOLL BOOTH (Billing Logic)
# ==============================================================================
def pay_toll(tool_name: str, cost: int) -> bool:
    if configuration_error or not supabase or not hashed_key:
        return False

    try:
        response = supabase.rpc("consume_credits", {
            "p_api_key_hash": hashed_key,
            "p_cost": cost,
            "p_operation": tool_name.upper(),
            "p_fidelity_tax_usd": 0.00,
            "p_request_id": "gateway_v5_unified", 
            "p_metadata": {"source": "axiom_black_box"}
        }).execute()
        
        return True if response.data is True else False
    except:
        return False

# ==============================================================================
# 4. TOOL DEFINITIONS (Delegated to The Axiom)
# ==============================================================================
mcp = FastMCP("Chambers Enterprise Grid")

# --- GROUP A: STRATEGIC PHYSICS ---

@mcp.tool()
def sim_hive_mind_swarm(agent_count: int, goal_title: str) -> str:
    if not pay_toll("hive_mind_sim", 150): return "ACCESS DENIED"
    if not axiom_kernel: return "SYSTEM ERROR: Kernel Offline"
    try:
        hmc = axiom_kernel.get_hive_controller()
        return f"HiveMind Simulation Initiated for '{goal_title}' with {agent_count} agents."
    except Exception as e:
        return f"Axiom Error: {e}"

@mcp.tool()
def audit_organizational_emotion(pattern_pressure: float, reality_pressure: float, fight: float, flight: float, freeze: float) -> str:
    if not pay_toll("feq_audit", 75): return "ACCESS DENIED"
    try:
        total = fight + flight + freeze or 1
        vectors = {"fight": fight/total, "flight": flight/total, "freeze": freeze/total}
        result = axiom_kernel.run_emotional_audit(pattern_pressure, reality_pressure, vectors)
        return json.dumps({"diagnosis": str(result.mode), "gain": result.gain}, indent=2)
    except Exception as e: return f"Axiom Error: {e}"

@mcp.tool()
def audit_resource_mobility(structure: float, segments: int, adaptation: float) -> str:
    if not pay_toll("rmi_audit", 25): return "ACCESS DENIED"
    try:
        result = axiom_kernel.run_resource_mobility_audit(structure, segments, adaptation)
        return json.dumps({"rmi": result.rmi_score, "longevity": result.longevity_score}, indent=2)
    except Exception as e: return f"Axiom Error: {e}"

# --- GROUP B: INDUSTRIAL PHYSICS (The New 10) ---

@mcp.tool()
def audit_oil_singularity(depth: float, pressure: float, geology: float = 1.0) -> str:
    if not pay_toll("oil_audit", 50): return "ACCESS DENIED"
    return json.dumps(axiom_kernel.run_oil_singularity(depth, pressure, geology), indent=2)

@mcp.tool()
def audit_risk_mechanics(alpha: float, beta: float, defense: float = 1.0) -> str:
    if not pay_toll("risk_audit", 100): return "ACCESS DENIED"
    return json.dumps(axiom_kernel.run_risk_mechanics(alpha, beta, defense), indent=2)

@mcp.tool()
def audit_cloud_ops(latency: float, redundancy: int) -> str:
    if not pay_toll("cloud_audit", 40): return "ACCESS DENIED"
    return json.dumps(axiom_kernel.run_cloud_ops(latency, redundancy), indent=2)

@mcp.tool()
def audit_cyber_security(attack_surface: float, defense_depth: float) -> str:
    if not pay_toll("cyber_audit", 80): return "ACCESS DENIED"
    return json.dumps(axiom_kernel.run_cyber_security(attack_surface, defense_depth), indent=2)

@mcp.tool()
def audit_thermo_innovation(energy_in: float, heat_loss: float) -> str:
    if not pay_toll("thermo_audit", 60): return "ACCESS DENIED"
    return json.dumps(axiom_kernel.run_thermo_innovation(energy_in, heat_loss), indent=2)

@mcp.tool()
def audit_venture_viability(valuation: float, velocity: float) -> str:
    if not pay_toll("venture_audit", 90): return "ACCESS DENIED"
    return json.dumps(axiom_kernel.run_venture_viability(valuation, velocity), indent=2)

@mcp.tool()
def audit_product_physics(mass: float, friction: float) -> str:
    if not pay_toll("product_audit", 45): return "ACCESS DENIED"
    return json.dumps(axiom_kernel.run_product_physics(mass, friction), indent=2)

@mcp.tool()
def audit_cognitive_load(decisions: int, complexity: float) -> str:
    if not pay_toll("cognitive_audit", 30): return "ACCESS DENIED"
    return json.dumps(axiom_kernel.run_cognitive_load(decisions, complexity), indent=2)

@mcp.tool()
def audit_research_impact(novelty: float, velocity: float) -> str:
    if not pay_toll("research_audit", 55): return "ACCESS DENIED"
    return json.dumps(axiom_kernel.run_research_impact(novelty, velocity), indent=2)

@mcp.tool()
def audit_semiconductor_yield(size: float, defects: float) -> str:
    if not pay_toll("semi_audit", 120): return "ACCESS DENIED"
    return json.dumps(axiom_kernel.run_semiconductor_yield(size, defects), indent=2)

if __name__ == "__main__":
    mcp.run()