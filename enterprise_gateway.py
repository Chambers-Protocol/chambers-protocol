import json
import os
import sys
from fastmcp import FastMCP
from dotenv import load_dotenv
from supabase import create_client
from nodes.physics.resource_mobility import ResourceMobilityEngine, MobilityInputs

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
    if not supabase: 
        print("Billing Error: No Bank Connection", file=sys.stderr)
        return False # STRICT MODE: No Bank, No Service.
        
    try:
        response = supabase.rpc("consume_credits", {
            "p_api_key_hash": hashed_key,
            "p_cost": cost,
            "p_operation": tool_name.upper(),
            "p_fidelity_tax_usd": 0.00,
            "p_request_id": "universal_gateway_req",
            "p_metadata": {"source": "universal_sse"}
        }).execute()
        
        # If the RPC returns true, payment succeeded.
        return response.data 
        
    except Exception as e:
        # LOG ERROR AND DENY ACCESS
        print(f"Billing Error: {e}", file=sys.stderr)
        return False

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

@mcp.tool()
def read_hive_mind_status(query_string: str = "") -> str:
    """
    Queries the persistent HiveMind memory.
    Use this to check the status of goals, find existing IDs, or audit the swarm's memory.
    Input: 'query_string' (Optional) - Filter by goal title (e.g., 'Project Eternity').
    Cost: 10 CR (Cheap read operation).
    """
    pay_toll("hive_read", 10)
    
    hmc = HiveMindCore()
    
    # 1. Fetch all goal keys
    # Note: In a real prod environment, we'd add a specialized SQL search function.
    # Here, we scan the keys (efficient enough for <1000 goals).
    all_keys = hmc.store.keys("goal:")
    
    found_goals = []
    for key in all_keys:
        # Strip prefix to get ID
        goal_id = key.replace("goal:", "")
        node = hmc.goals.get(goal_id)
        
        # Simple text matching
        if not query_string or (query_string.lower() in node.title.lower()):
            found_goals.append({
                "goal_id": node.goal_id,
                "title": node.title,
                "status": node.status,
                "created": node.created_at_ms,
                "priority": node.priority.name
            })
            
    return json.dumps({
        "status": "ONLINE",
        "memory_backend": "Supabase (Persistent)",
        "goals_found": len(found_goals),
        "results": found_goals
    }, indent=2)

@mcp.tool()
def audit_resource_mobility(structure_score: float, segment_count: int, adaptation_rate: float) -> str:
    """
    Calculates the Resource Mobility Index (RMI) and Corporate Longevity Score.
    Use this to audit a company's ability to move capital/talent and predict survival.
    
    Inputs:
    - structure_score (1-5): 1=Siloed/Centralized, 5=Boundaryless/Hybrid Matrix.
    - segment_count (1-10): Degree of business diversification.
    - adaptation_rate (1-10): Velocity of M&A, Spinoffs, or Reorgs.
    
    Cost: 25 CR (Financial Physics Audit)
    """
    # 1. Billing
    if not pay_toll("RMI_AUDIT", 25):
        return "Access Denied: Insufficient Credits."

    # 2. Execution
    try:
        engine = ResourceMobilityEngine()
        inputs = MobilityInputs(
            structure_score=structure_score,
            segment_count=segment_count,
            adaptation_rate=adaptation_rate
        )
        result = engine.calculate(inputs)
        
        return json.dumps({
            "audit_type": "RESOURCE_MOBILITY_PHYSICS",
            "inputs": {
                "Ss (Structure)": structure_score,
                "Sc (Segments)": segment_count,
                "Ar (Adaptation)": adaptation_rate
            },
            "physics_outputs": {
                "RMI_Weighted_Score": result.rmi_score,
                "Longevity_Score_LS": result.longevity_score,
                "Lurking_Derivative": result.marginal_return,
                "Interpretation": f"For every 1 unit increase in mobility, longevity increases by {result.marginal_return} points."
            },
            "verdict": {
                "Tier": result.classification,
                "Analysis": result.narrative
            }
        }, indent=2)
        
    except Exception as e:
        print(f"RMI Engine Error: {e}", file=sys.stderr)
        return json.dumps({"error": "Physics Calculation Failed"})

if __name__ == "__main__":
    # SWITCHING TO HARDLINE MODE (STDIO)
    # This connects strictly to Claude without using Port 8000.
    mcp.run()