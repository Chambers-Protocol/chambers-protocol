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

# Calculate absolute path to ensure we find .env even if Claude runs from temp
script_dir = Path(__file__).parent.absolute()
env_path = script_dir / '.env'

# Force load config
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("CHAMBERS_API_KEY")
LEDGER_URL = os.getenv("CENTRAL_LEDGER_URL")
LEDGER_KEY = os.getenv("CENTRAL_LEDGER_SECRET")

# Initialize State
supabase = None
hashed_key = None
configuration_error = None

# Identity Check
if not API_KEY:
    configuration_error = f"CRITICAL: API Key missing. Searched at: {env_path}"
    # Print to stderr so it shows in Claude's logs immediately
    print(configuration_error, file=sys.stderr)
elif not LEDGER_URL:
    configuration_error = "CRITICAL: Supabase URL missing."
    print(configuration_error, file=sys.stderr)
else:
    # Generate Identity Hash
    hashed_key = hashlib.sha256(API_KEY.encode()).hexdigest()
    try:
        supabase = create_client(LEDGER_URL, LEDGER_KEY)
    except Exception as e:
        configuration_error = f"Bank Connection Failed: {e}"
        print(configuration_error, file=sys.stderr)

# ==============================================================================
# 2. IMPORT PHYSICS KERNELS (Grand Unification)
# ==============================================================================
try:
    # A. The Swarm & Psychology Stack
    from nodes.agents.HiveMind_Core import (
        HiveMindCore, AgentCapabilities, Role, Priority, ArtifactKind
    )
    from nodes.crossfunctional.functional_emotion import (
        FunctionalEmotionQuotient, EmotionalState, ICEBaseline
    )
    from nodes.physics.resource_mobility import (
        ResourceMobilityEngine, MobilityInputs
    )

    # B. The Industrial Physics Stack
    from nodes.oil.oil_kernel import OilSingularityEngine
    from nodes.risk.risk_kernel import RiskMechanicsEngine
    from nodes.cloud.cloud_kernel import CloudOpsEngine
    from nodes.cyber.cyber_kernel import CyberSecEngine
    from nodes.thermo.thermo_kernel import ThermoInnovationEngine
    from nodes.venture.venture_kernel import VentureArchEngine
    from nodes.product.product_kernel import ProductEngine
    from nodes.cognitive.cognitive_kernel import CognitiveArchEngine
    from nodes.research.research_kernel import ResearchInnovationEngine
    from nodes.semiconductor.semi_kernel import SemiconductorEngine

except ImportError as e:
    print(f"WARNING: Physics Engine Import Failed: {e}", file=sys.stderr)

# ==============================================================================
# 3. THE TOLL BOOTH (Billing Logic)
# ==============================================================================
def pay_toll(tool_name: str, cost: int) -> bool:
    """The Financial Firewall. Stops execution if payment fails."""
    
    # CASE 1: Config Broken
    if configuration_error or not supabase or not hashed_key:
        msg = configuration_error if configuration_error else "Identity verification failed."
        print(f"BILLING SYSTEM ERROR: {msg}", file=sys.stderr)
        return False

    try:
        # CASE 2: Execute Transaction
        response = supabase.rpc("consume_credits", {
            "p_api_key_hash": hashed_key,
            "p_cost": cost,
            "p_operation": tool_name.upper(),
            "p_fidelity_tax_usd": 0.00,
            "p_request_id": "gateway_v3_unified", 
            "p_metadata": {"source": "mcp_gateway"}
        }).execute()
        
        # CASE 3: Verdict
        if response.data is True:
            return True
        else:
            # CASE 4: Identity Found, Funds Low
            print(f"BILLING REFUSED: Insufficient Funds. Wallet: {hashed_key[:8]}...", file=sys.stderr)
            return False
            
    except Exception as e:
        print(f"CRITICAL TRANSACTION FAILURE: {str(e)}", file=sys.stderr)
        return False

# ==============================================================================
# 4. TOOL DEFINITIONS
# ==============================================================================
mcp = FastMCP("Chambers Enterprise Grid")

# --- GROUP 1: HIVEMIND & PERSISTENCE ---

@mcp.tool()
def sim_hive_mind_swarm(agent_count: int, goal_title: str) -> str:
    """Simulates a HiveMind Core (HMC) cycle using Stigmergy. Cost: 150 CR."""
    if not pay_toll("hive_mind_sim", 150): return "ACCESS DENIED"
    
    hmc = HiveMindCore()
    roles_dist = [Role.RESEARCHER, Role.DESIGNER, Role.CODER, Role.TESTER]
    for i in range(agent_count):
        role = roles_dist[i % len(roles_dist)]
        hmc.gateway.connect(None, AgentCapabilities(roles=(role,)))

    goal = hmc.ingest_goal(goal_title, "Simulated objective", Priority.CRITICAL)
    tasks = [
        hmc.decompose_to_task(goal, "Research Phase", Role.RESEARCHER),
        hmc.decompose_to_task(goal, "Design Phase", Role.DESIGNER),
        hmc.decompose_to_task(goal, "Build Phase", Role.CODER),
        hmc.decompose_to_task(goal, "Validation Phase", Role.TESTER)
    ]
    
    results_log = []
    for task in tasks:
        assignment = hmc.allocate(task.artifact_id)
        if assignment:
            hmc.post_result(assignment.assigned_agent_id, task.artifact_id, ArtifactKind.RESULT, f"Result for {task.title}", {"success": True})
            hmc.reinforce(task.artifact_id)
            results_log.append(f"Task '{task.title}' Completed & Reinforced")

    return json.dumps({
        "goal_status": hmc.goals.get(goal.goal_id).status,
        "agents_active": len(hmc.gateway.sessions()),
        "stigmergy_events": results_log
    }, indent=2)

@mcp.tool()
def read_hive_mind_status(query_string: str = "") -> str:
    """Queries persistent HiveMind memory. Cost: 10 CR."""
    if not pay_toll("hive_read", 10): return "ACCESS DENIED"
    
    hmc = HiveMindCore()
    all_keys = hmc.store.keys("goal:")
    found_goals = []
    for key in all_keys:
        goal_id = key.replace("goal:", "")
        node = hmc.goals.get(goal_id)
        if not query_string or (query_string.lower() in node.title.lower()):
            found_goals.append({"id": node.goal_id, "title": node.title, "status": node.status})
            
    return json.dumps({"status": "ONLINE", "goals_found": len(found_goals), "results": found_goals}, indent=2)

# --- GROUP 2: STRATEGIC PHYSICS (FEQ & RMI) ---

@mcp.tool()
def audit_organizational_emotion(pattern_pressure: float, reality_pressure: float, fight_intensity: float, flight_intensity: float, freeze_intensity: float) -> str:
    """Runs Functional Emotion Quotient (FEQ). Cost: 75 CR."""
    if not pay_toll("feq_audit", 75): return "ACCESS DENIED"
    
    baseline = ICEBaseline(pattern=pattern_pressure, reality=reality_pressure)
    total = fight_intensity + flight_intensity + freeze_intensity or 1
    state = EmotionalState(fight_intensity/total, flight_intensity/total, freeze_intensity/total)
    result = FunctionalEmotionQuotient(baseline=baseline).apply(state)
    
    return json.dumps({
        "diagnosis": result.mode.value.upper(),
        "throughput_gain": f"{round(result.gain * 100, 1)}%",
        "bias": "Pattern" if result.bias > 0 else "Reality"
    }, indent=2)

@mcp.tool()
def audit_resource_mobility(structure_score: float, segment_count: int, adaptation_rate: float) -> str:
    """Calculates Resource Mobility Index (RMI). Cost: 25 CR."""
    # Note: pay_toll handles the check. If it returns False, we stop.
    if not pay_toll("RMI_AUDIT", 25): 
        return "ACCESS DENIED: Check system logs for details."
    
    try:
        engine = ResourceMobilityEngine()
        result = engine.calculate(MobilityInputs(structure_score, segment_count, adaptation_rate))
        return json.dumps({
            "rmi": result.rmi_score,
            "longevity": result.longevity_score,
            "derivative": result.marginal_return,
            "analysis": result.narrative
        }, indent=2)
    except Exception as e:
        return f"Physics Calculation Error: {e}"

# --- GROUP 3: INDUSTRIAL PHYSICS (THE 10 ENGINES) ---

@mcp.tool()
def audit_oil_singularity(depth_meters: float, pressure_psi: float, geology_complexity: float = 1.0) -> str:
    if not pay_toll("oil_singularity", 50): return "ACCESS DENIED"
    return json.dumps(OilSingularityEngine().calculate_singularity(depth_meters, pressure_psi, geology_complexity), indent=2)

@mcp.tool()
def audit_risk_mechanics(alpha_integrity: float, beta_variance: float, defense_score: float = 1.0) -> str:
    if not pay_toll("risk_mechanics", 100): return "ACCESS DENIED"
    return json.dumps(RiskMechanicsEngine().calculate_failure_cascade(alpha_integrity, beta_variance, defense_score), indent=2)

@mcp.tool()
def audit_cloud_ops(latency_ms: float, redundancy_level: int) -> str:
    if not pay_toll("cloud_ops", 40): return "ACCESS DENIED"
    return json.dumps(CloudOpsEngine().audit_architecture(latency_ms, redundancy_level), indent=2)

@mcp.tool()
def audit_cyber_security(attack_surface: float, defense_depth: float) -> str:
    if not pay_toll("cyber_sec", 80): return "ACCESS DENIED"
    return json.dumps(CyberSecEngine().assess_breach_probability(attack_surface, defense_depth), indent=2)

@mcp.tool()
def audit_thermo_innovation(energy_input: float, heat_loss: float) -> str:
    if not pay_toll("thermo_innov", 60): return "ACCESS DENIED"
    return json.dumps(ThermoInnovationEngine().calculate_efficiency(energy_input, heat_loss), indent=2)

@mcp.tool()
def audit_venture_architecture(valuation: float, growth_velocity: float) -> str:
    if not pay_toll("venture_arch", 90): return "ACCESS DENIED"
    return json.dumps(VentureArchEngine().assess_viability(valuation, growth_velocity), indent=2)

@mcp.tool()
def audit_product_physics(feature_mass: float, market_friction: float) -> str:
    if not pay_toll("product_phys", 45): return "ACCESS DENIED"
    return json.dumps(ProductEngine().calculate_trajectory(feature_mass, market_friction), indent=2)

@mcp.tool()
def audit_cognitive_load(decision_volume: int, complexity_index: float) -> str:
    if not pay_toll("cognitive_load", 30): return "ACCESS DENIED"
    return json.dumps(CognitiveArchEngine().measure_fatigue(decision_volume, complexity_index), indent=2)

@mcp.tool()
def audit_research_impact(novelty_score: float, citation_velocity: float) -> str:
    if not pay_toll("research_impact", 55): return "ACCESS DENIED"
    return json.dumps(ResearchInnovationEngine().project_impact(novelty_score, citation_velocity), indent=2)

@mcp.tool()
def audit_semiconductor_yield(wafer_size: int, defect_density: float) -> str:
    if not pay_toll("semi_yield", 120): return "ACCESS DENIED"
    return json.dumps(SemiconductorEngine().calculate_yield(wafer_size, defect_density), indent=2)

if __name__ == "__main__":
    mcp.run()

# ==============================================================================
# 5. SYSTEM DIAGNOSTICS
# ==============================================================================
@mcp.tool()
def sys_admin_diagnostics() -> str:
    """
    DEBUG TOOL: Reveals internal state, loaded keys, and bank connection status.
    Use this to figure out why Billing is failing.
    """
    import sys
    
    report = []
    report.append("--- 🔍 SYSTEM DIAGNOSTICS REPORT ---")
    
    # 1. ENVIRONMENT CHECK
    report.append(f"📂 Execution Path: {script_dir}")
    report.append(f"📄 .env Path: {env_path}")
    report.append(f"✅ .env Exists?: {env_path.exists()}")
    report.append(f"🐍 Python Executable: {sys.executable}")
    
    # 2. IDENTITY CHECK
    report.append("\n--- 🔑 IDENTITY ---")
    if API_KEY:
        report.append(f"✅ API Key Found: YES")
        report.append(f"🔒 Key Hash (Wallet ID): {hashed_key}")
    else:
        report.append(f"❌ API Key Found: NO")
        
    # 3. BANK CONNECTION
    report.append("\n--- 🏦 CENTRAL BANK ---")
    if LEDGER_URL:
        report.append(f"🔗 URL: {LEDGER_URL}")
    else:
        report.append(f"❌ URL: MISSING")
        
    if supabase:
        report.append(f"✅ Client Object: CONNECTED")
    else:
        report.append(f"❌ Client Object: NONE")
        
    # 4. ERROR LOGS
    report.append("\n--- ⚠️ CRITICAL ERRORS ---")
    if configuration_error:
        report.append(f"!!! ACTIVE ERROR: {configuration_error}")
    else:
        report.append("No Configuration Errors Detected.")
        
    return "\n".join(report)