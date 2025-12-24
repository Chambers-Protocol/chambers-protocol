# enterprise_gateway.py
import os
import uvicorn
import hashlib
from dotenv import load_dotenv
from fastmcp import FastMCP
from supabase import create_client

# --- 1. SETUP SECURITY & BILLING ---
load_dotenv()
API_KEY = os.getenv("CHAMBERS_API_KEY")
LEDGER_URL = os.getenv("CENTRAL_LEDGER_URL")
LEDGER_KEY = os.getenv("CENTRAL_LEDGER_SECRET")

if not API_KEY or not LEDGER_URL:
    print("❌ SECURITY FATAL: .env file missing API Keys. Server halting.")
    exit()

# Connect to the Bank
supabase = create_client(LEDGER_URL, LEDGER_KEY)
hashed_key = hashlib.sha256(API_KEY.encode()).hexdigest()

def pay_toll(tool_name: str, cost: int):
    """The Toll Booth. Stops execution if payment fails."""
    try:
        response = supabase.rpc("consume_credits", {
            "p_api_key_hash": hashed_key,
            "p_cost": cost,
            "p_operation": tool_name.upper(),
            "p_fidelity_tax_usd": 0.00,
            "p_request_id": "universal_gateway_req", 
            "p_metadata": {"source": "universal_sse"}
        }).execute()
        
        # If the procedure returns TRUE, payment succeeded.
        # If user is broke, the database usually raises an error or returns false.
        print(f"💰 TOLL PAID: {cost} CR for {tool_name}")
        return True
    except Exception as e:
        print(f"🛑 BILLING FAILED: {e}")
        raise ValueError("⛔ INSUFFICIENT CREDITS: Please recharge your Chambers License.")

# --- 2. IMPORT THE PHYSICS KERNELS ---
try:
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
except ImportError as e:
    print(f"❌ CRITICAL IMPORT ERROR: {e}")
    exit()

# --- 3. INITIALIZE SERVER ---
mcp = FastMCP("Chambers Enterprise Gateway")

# --- 4. EXPOSE TOOLS (WITH BILLING HOOKS) ---

@mcp.tool()
def audit_oil_singularity(depth_meters: float, pressure_psi: float, geology_complexity: float = 1.0) -> float:
    """Calculates extraction difficulty. Cost: 50 CR."""
    pay_toll("oil_singularity", 50) # <--- THE PAYWALL
    return OilSingularityEngine().calculate_singularity(depth_meters, pressure_psi, geology_complexity)

@mcp.tool()
def audit_risk_mechanics(alpha_integrity: float, beta_variance: float, defense_score: float = 1.0) -> float:
    """Calculates failure probability. Cost: 100 CR."""
    pay_toll("risk_mechanics", 100)
    return RiskMechanicsEngine().calculate_failure_cascade(alpha_integrity, beta_variance, defense_score)

@mcp.tool()
def audit_venture_viability(team_score: float, market_size: float, product_fit: float = 1.0) -> float:
    """Calculates valuation velocity. Cost: 100 CR."""
    pay_toll("venture_viability", 100)
    return VentureArchEngine().calculate_velocity(team_score, market_size, product_fit)

@mcp.tool()
def audit_thermo_innovation(efficiency_claimed: float, heat_loss_factor: float = 0.1) -> float:
    """Validates energy efficiency. Cost: 50 CR."""
    pay_toll("thermo_innovation", 50)
    return ThermoInnovationEngine().validate_efficiency(efficiency_claimed, heat_loss_factor)

@mcp.tool()
def audit_cognitive_psych(leadership_stability: float, bias_index: float = 0.0) -> float:
    """Profiles leadership stability. Cost: 100 CR."""
    pay_toll("cognitive_psych", 100)
    return CognitiveArchEngine().profile_leadership(leadership_stability, bias_index)

@mcp.tool()
def audit_cloud_ops(uptime_sre: float, latency_ms: float, cost_efficiency: float) -> float:
    """Audits digital reliability. Cost: 10 CR."""
    pay_toll("cloud_ops", 10)
    return CloudOpsEngine().audit_reliability(uptime_sre, latency_ms, cost_efficiency)

@mcp.tool()
def audit_cyber_shield(posture_score: float, threat_level: float) -> float:
    """Calculates defense scores. Cost: 10 CR."""
    pay_toll("cyber_shield", 10)
    return CyberSecEngine().calculate_defense(posture_score, threat_level)

@mcp.tool()
def audit_semiconductor_yield(lithography_precision: float, purity_index: float) -> float:
    """Calculates chip yield. Cost: 50 CR."""
    pay_toll("semiconductor_yield", 50)
    return SemiconductorEngine().calculate_yield(lithography_precision, purity_index)

@mcp.tool()
def audit_product_strategy(strategy_clarity: float, execution_velocity: float) -> float:
    """Calculates product success. Cost: 100 CR."""
    pay_toll("product_strategy", 100)
    return ProductEngine().calculate_pipeline(strategy_clarity, execution_velocity)

@mcp.tool()
def audit_research_hpqai(quantum_readiness: float, ai_compute: float) -> float:
    """Audits R&D convergence. Cost: 10 CR."""
    pay_toll("research_hpqai", 10)
    return ResearchInnovationEngine().calculate_convergence(quantum_readiness, ai_compute)

# --- 5. LAUNCH ---
if __name__ == "__main__":
    print("💎 CHAMBERS ENTERPRISE GATEWAY: SECURE")
    print("💰 TOLL SYSTEM: ACTIVE (Connected to Supabase)")
    print("📡 Listening for SSE Connections on http://0.0.0.0:8000")
    mcp.run(transport="sse")