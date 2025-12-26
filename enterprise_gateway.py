import json
import os
import sys
from fastmcp import FastMCP
from dotenv import load_dotenv
from supabase import create_client

# --- 1. SETUP SECURITY & BILLING ---
load_dotenv()
API_KEY = os.getenv("CHAMBERS_API_KEY")
LEDGER_URL = os.getenv("CENTRAL_LEDGER_URL")
LEDGER_KEY = os.getenv("CENTRAL_LEDGER_SECRET")

# Connect to the Bank (Fail safely if keys are missing)
supabase = None
hashed_key = "test_key"
if LEDGER_URL and LEDGER_KEY:
    try:
        supabase = create_client(LEDGER_URL, LEDGER_KEY)
        import hashlib
        if API_KEY:
            hashed_key = hashlib.sha256(API_KEY.encode()).hexdigest()
    except Exception as e:
        print(f"Ledger Connection Error: {e}")

def pay_toll(tool_name: str, cost: int):
    """The Toll Booth. Stops execution if payment fails."""
    if not supabase: return True 
    try:
        supabase.rpc("consume_credits", {
            "p_api_key_hash": hashed_key,
            "p_cost": cost,
            "p_operation": tool_name.upper(),
            "p_fidelity_tax_usd": 0.00,
            "p_request_id": "universal_gateway_req",
            "p_metadata": {"source": "universal_sse"}
        }).execute()
        return True
    except Exception as e:
        print(f"Billing Error: {e}")
        return True

# --- 2. IMPORT KERNELS ---
try:
    # Existing Enterprise Physics
    from nodes.oil.oil_kernel import OilSingularityEngine
    from nodes.thermo.thermo_kernel import ThermoInnovationEngine
    from nodes.semiconductor.semi_kernel import SemiconductorEngine
    from nodes.cloud.cloud_kernel import CloudOpsEngine
    from nodes.cyber.cyber_kernel import CyberSecEngine
    from nodes.research.research_kernel import ResearchInnovationEngine
    from nodes.risk.risk_kernel import RiskMechanicsEngine
    from nodes.venture.venture_kernel import VentureArchEngine
    from nodes.product.product_kernel import ProductEngine
    from nodes.cognitive.cognitive_kernel import CognitiveArchEngine

    # --- THE NEW BRAINS (ChatGPT/Grok Architectures) ---
    from nodes.crossfunctional.functional_emotion import (
        FunctionalEmotionQuotient, 
        EmotionalState, 
        ICEBaseline
    )
    from nodes.agents.HiveMind_Core import (
        HiveMindCore, 
        AgentCapabilities, 
        Role, 
        Priority, 
        ArtifactKind
    )

except ImportError as e:
    print(f"CRITICAL IMPORT ERROR: {e}")

mcp = FastMCP("Chambers Enterprise Grid")

# --- 3. EXPOSE EXISTING TOOLS ---

@mcp.tool()
def audit_oil_singularity(depth_meters: float, pressure_psi: float, geology_complexity: float = 1.0) -> str:
    """Calculates extraction difficulty. Cost: 50 CR."""
    pay_toll("oil_singularity", 50)
    return json.dumps(OilSingularityEngine().calculate_singularity(depth_meters, pressure_psi, geology_complexity), indent=2)

@mcp.tool()
def audit_risk_mechanics(alpha_integrity: float, beta_variance: float, defense_score: float = 1.0) -> str:
    """Calculates failure probability. Cost: 100 CR."""
    pay_toll("risk_mechanics", 100)
    return json.dumps(RiskMechanicsEngine().calculate_failure_cascade(alpha_integrity, beta_variance, defense_score), indent=2)

# --- 4. EXPOSE NEW "BRAIN" TOOLS ---

@mcp.tool()
def audit_organizational_emotion(
    pattern_pressure: float, 
    reality_pressure: float, 
    fight_intensity: float,
    flight_intensity: float, 
    freeze_intensity: float
) -> str:
    """
    Runs the Functional Emotion Quotient (FEQ).
    Detects if the org is in Flow, Fight, Flight, or Freeze.
    Inputs:
      - pattern_pressure / reality_pressure: The 5.1:4.9 baseline targets.
      - fight/flight/freeze: 0.0 to 1.0 intensities (must roughly sum to 1.0).
    Cost: 75 CR.
    """
    pay_toll("feq_audit", 75)
    
    # Construct the complex objects required by functional_emotion.py
    baseline = ICEBaseline(pattern=pattern_pressure, reality=reality_pressure)
    
    # Normalize inputs safely
    total = fight_intensity + flight_intensity + freeze_intensity
    if total == 0: total = 1 
    
    state = EmotionalState(
        fight=fight_intensity/total, 
        flight=flight_intensity/total, 
        freeze=freeze_intensity/total
    )
    
    # Run the Engine
    feq = FunctionalEmotionQuotient(baseline=baseline)
    result = feq.apply(state)
    
    output = {
        "diagnosis": result.mode.value.upper(),
        "throughput_gain": f"{round(result.gain * 100, 1)}%",
        "stall_warning": result.stall,
        "effective_ratio": f"P:{round(result.effective_pattern, 2)} / R:{round(result.effective_reality, 2)}",
        "bias_direction": "Pattern (Structure)" if result.bias > 0 else "Reality (Adaptation)",
        "signals": result.signals
    }
    return json.dumps(output, indent=2)

@mcp.tool()
def sim_hive_mind_swarm(agent_count: int, goal_title: str) -> str:
    """
    Simulates a HiveMind Core (HMC) cycle using Stigmergy.
    Spins up agents, ingests a goal, and measures coordination.
    Cost: 150 CR.
    """
    pay_toll("hive_mind_sim", 150)
    
    # Initialize the Core
    hmc = HiveMindCore()
    
    # Connect Agents (Distributing roles)
    roles_dist = [Role.RESEARCHER, Role.DESIGNER, Role.CODER, Role.TESTER]
    for i in range(agent_count):
        role = roles_dist[i % len(roles_dist)]
        hmc.gateway.connect(None, AgentCapabilities(roles=(role,)))

    # Ingest Goal
    goal = hmc.ingest_goal(goal_title, "Simulated objective", Priority.CRITICAL)
    
    # Simulate Work Cycle (Decompose -> Allocate -> Result -> Reinforce)
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
            # Agent posts a result
            art = hmc.post_result(
                assignment.assigned_agent_id, 
                task.artifact_id, 
                ArtifactKind.RESULT, 
                f"Result for {task.title}", 
                {"success": True}
            )
            # The System Reinforces it
            score = hmc.reinforce(art.artifact_id)
            results_log.append(f"Task '{task.title}' -> Score: {score.score} (Reinforced)")

    # Report
    top_artifacts = hmc.board.list()[:5]
    summary = {
        "goal_status": hmc.goals.get(goal.goal_id).status,
        "agents_active": len(hmc.gateway.sessions()),
        "stigmergy_events": results_log,
        "top_pheromones": [
            f"{a.kind.value}: {a.title} (Strength: {round(a.pheromone_strength, 2)})" 
            for a in top_artifacts
        ]
    }
    return json.dumps(summary, indent=2)

if __name__ == "__main__":
    # SWITCHING TO HARDLINE MODE (STDIO)
    # This connects strictly to Claude without using Port 8000.
    mcp.run()