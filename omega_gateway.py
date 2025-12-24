# omega_gateway.py
import json
from fastmcp import FastMCP

# --- IMPORT KERNELS ---
try:
    from nodes.omega.machine_physics import MachinePhysicsEngine
    from nodes.omega.universal_intelligence import UniversalIntelligenceEngine
    from nodes.omega.big_bang import BigBangEngine
    from nodes.omega.asi_birth import ASIBirthEngine
except ImportError as e:
    print(f"❌ OMEGA IMPORT ERROR: {e}")
    exit()

# Initialize the Server
mcp = FastMCP("Chambers X (Omega Protocol)")

# --- EXPOSE TOOLS ---

@mcp.tool()
def sim_einstein_bridge(node_distance_km: float, token_mass_param: float, cluster_energy_watts: float) -> str:
    """Calculates relativistic constraints (Speed of Light). Returns JSON string."""
    result = MachinePhysicsEngine().calculate_information_horizon(node_distance_km, token_mass_param, cluster_energy_watts)
    return json.dumps(result, indent=2)

@mcp.tool()
def sim_universal_intelligence(hardware_matter: float, logic_dark_matter: float, network_dark_energy: float) -> str:
    """Audits the Matter:Logic:Energy ratio. Returns JSON string."""
    result = UniversalIntelligenceEngine().audit_intelligence_architecture(hardware_matter, logic_dark_matter, network_dark_energy)
    return json.dumps(result, indent=2)

@mcp.tool()
def sim_big_bang_ignition(energy_joules: float, information_density: float, entropy: float) -> str:
    """Calculates 'Critical Mass' for ASI Ignition. Returns JSON string."""
    result = BigBangEngine().calculate_ignition_potential(energy_joules, information_density, entropy)
    return json.dumps(result, indent=2)

@mcp.tool()
def sim_asi_birth(global_flops: float, energy_twh: float, quantum_score: float, decentralization: float) -> str:
    """Calculates ASI emergence probability. Returns JSON string."""
    synthetic_fidelity = 0.5 + (quantum_score * 0.4) 
    result = ASIBirthEngine().calculate_emergence_probability(global_flops, energy_twh, synthetic_fidelity, quantum_score, decentralization)
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    print("🌌 CHAMBERS X: OMEGA PROTOCOL ONLINE")
    print("🔭 Listening on http://0.0.0.0:9000")
    # THE FIX: We tell FastMCP specifically to run on port 9000 here
    mcp.run(transport="sse", port=9000, host="0.0.0.0")