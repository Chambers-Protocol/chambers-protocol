"""
CHAMBERS PROTOCOL: ENTERPRISE GRID CONTROLLER
The Unified Interface for the Chambers Constellation.
One Key. All Nodes.
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
from mcp.server.fastmcp import FastMCP

# --- 1. IMPORT THE PHYSICS ENGINES (KERNELS) ---
# We import the logic directly, skipping the individual server wrappers.
sys.path.append(os.path.join(os.path.dirname(__file__), 'nodes'))

from nodes.risk.risk_kernel import RiskMechanicsEngine
from nodes.oil.oil_kernel import OilSingularityEngine
from nodes.cloud.cloud_kernel import CloudOpsEngine
from nodes.cyber.cyber_kernel import CyberSecEngine
from nodes.thermo.thermo_kernel import ThermoInnovationEngine
from nodes.venture.venture_kernel import VentureArchEngine
from nodes.cognitive.cognitive_kernel import CognitiveArchEngine
from nodes.product.product_kernel import ProductEngine
from nodes.research.research_kernel import ResearchInnovationEngine
from nodes.semiconductor.semi_kernel import SemiconductorEngine

# --- 2. CONFIGURATION ---
# Detect if running as frozen executable (Installer) or script
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("CENTRAL_LEDGER_URL")
SUPABASE_KEY = os.getenv("CENTRAL_LEDGER_SECRET")
NODE_API_KEY = os.getenv("CHAMBERS_API_KEY")

# --- 3. INITIALIZE THE GRID ---
mcp = FastMCP("Chambers Enterprise Grid")

# Spin up all engines
engines = {
    "risk": RiskMechanicsEngine(),
    "oil": OilSingularityEngine(),
    "cloud": CloudOpsEngine(),
    "cyber": CyberSecEngine(),
    "thermo": ThermoInnovationEngine(),
    "venture": VentureArchEngine(),
    "cognitive": CognitiveArchEngine(),
    "product": ProductEngine(),
    "research": ResearchInnovationEngine(),
    "semi": SemiconductorEngine()
}

# Connect to Ledger
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ ENTERPRISE GRID: Connected to Central Ledger")
    print(f"🚀 ACTIVE NODES: {len(engines)} Physics Engines Online")
except Exception as e:
    print(f"❌ FATAL: Ledger Connection Failed - {e}")
    sys.exit(1)

# --- 4. UNIFIED BILLING GATE ---
def bill_usage(node_name: str, cost=10):
    """
    One function to bill them all.
    """
    if not NODE_API_KEY: return False
    hashed_key = hashlib.sha256(NODE_API_KEY.encode()).hexdigest()
    
    try:
        response = supabase.rpc("consume_credits", {
            "p_api_key_hash": hashed_key,
            "p_cost": cost,
            "p_operation": f"{node_name.upper()}_COMPUTE",
            "p_fidelity_tax_usd": 0.01,
            "p_request_id": None, 
            "p_metadata": {"node": node_name, "mode": "enterprise_grid"}
        }).execute()
        return response.data
    except Exception as e:
        print(f"Billing Error ({node_name}): {e}")
        return False

# --- 5. REGISTER ALL TOOLS ---

# --- NODE 1: RISK ---
@mcp.tool()
def risk_audit(inputs: str) -> str:
    """Run the Risk Mechanics Node. Input must be a JSON string of risk parameters."""
    if not bill_usage("risk"): return "⛔ Insufficient Credits."
    try:
        data = json.loads(inputs)
        return json.dumps(engines["risk"].compute_risk_fidelity(data), indent=2)
    except: return "Error: Invalid JSON input."

# --- NODE 2: OIL & GAS ---
@mcp.tool()
def oil_singularity(inputs: str) -> str:
    """Run the Oil & Gas Singularity Node. Input must be a JSON string."""
    if not bill_usage("oil"): return "⛔ Insufficient Credits."
    try:
        data = json.loads(inputs)
        return json.dumps(engines["oil"].compute_singularity_index(data), indent=2)
    except: return "Error: Invalid JSON input."

# --- NODE 3: CLOUD OPS ---
@mcp.tool()
def cloud_ops_audit(inputs: str) -> str:
    """Run the Cloud Operations Node. Input must be a JSON string."""
    if not bill_usage("cloud"): return "⛔ Insufficient Credits."
    try:
        data = json.loads(inputs)
        return json.dumps(engines["cloud"].compute_cloud_fidelity(data), indent=2)
    except: return "Error: Invalid JSON input."

# --- NODE 4: CYBERSECURITY ---
@mcp.tool()
def cyber_shield_audit(inputs: str) -> str:
    """Run the Cybersecurity Node. Input must be a JSON string."""
    if not bill_usage("cyber"): return "⛔ Insufficient Credits."
    try:
        data = json.loads(inputs)
        return json.dumps(engines["cyber"].compute_security_posture(data), indent=2)
    except: return "Error: Invalid JSON input."

# --- NODE 5: THERMOELECTRIC ---
@mcp.tool()
def thermo_innovation_audit(inputs: str) -> str:
    """Run the Thermoelectric Innovation Node. Input must be a JSON string."""
    if not bill_usage("thermo"): return "⛔ Insufficient Credits."
    try:
        data = json.loads(inputs)
        return json.dumps(engines["thermo"].compute_thermo_fidelity(data), indent=2)
    except: return "Error: Invalid JSON input."

# --- NODE 6: VENTURE ARCHITECTURE ---
@mcp.tool()
def venture_viability_audit(inputs: str) -> str:
    """Run the Venture Architecture Node. Input must be a JSON string."""
    if not bill_usage("venture"): return "⛔ Insufficient Credits."
    try:
        data = json.loads(inputs)
        return json.dumps(engines["venture"].compute_venture_valuation(data), indent=2)
    except: return "Error: Invalid JSON input."

# --- NODE 7: COGNITIVE FRAMEWORK ---
@mcp.tool()
def cognitive_psych_audit(inputs: str) -> str:
    """Run the Cognitive Psychology Node. Input must be a JSON string."""
    if not bill_usage("cognitive"): return "⛔ Insufficient Credits."
    try:
        data = json.loads(inputs)
        return json.dumps(engines["cognitive"].compute_cognitive_physics(data), indent=2)
    except: return "Error: Invalid JSON input."

# --- NODE 8: PRODUCT STRATEGY ---
@mcp.tool()
def product_strategy_audit(inputs: str) -> str:
    """Run the Product Strategy Node. Input must be a JSON string."""
    if not bill_usage("product"): return "⛔ Insufficient Credits."
    try:
        data = json.loads(inputs)
        return json.dumps(engines["product"].compute_product_viability(data), indent=2)
    except: return "Error: Invalid JSON input."

# --- NODE 9: RESEARCH (HPQAI) ---
@mcp.tool()
def research_hpqai_audit(inputs: str) -> str:
    """Run the Research & HPQAI Node. Input must be a JSON string."""
    if not bill_usage("research"): return "⛔ Insufficient Credits."
    try:
        data = json.loads(inputs)
        return json.dumps(engines["research"].compute_innovation_potential(data), indent=2)
    except: return "Error: Invalid JSON input."

# --- NODE 10: SEMICONDUCTOR ---
@mcp.tool()
def semiconductor_fab_audit(inputs: str) -> str:
    """Run the Semiconductor Sustainability Node. Input must be a JSON string."""
    if not bill_usage("semi"): return "⛔ Insufficient Credits."
    try:
        data = json.loads(inputs)
        return json.dumps(engines["semi"].compute_chip_viability(data), indent=2)
    except: return "Error: Invalid JSON input."

# --- 6. LAUNCH ---
if __name__ == "__main__":
    print("💎 CHAMBERS ENTERPRISE GRID: ONLINE")
    mcp.run()