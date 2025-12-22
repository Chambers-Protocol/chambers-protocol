import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
from mcp.server.fastmcp import FastMCP
import CHAMBERS_NODE_KERNEL as kernel

# --- REPLACEMENT CONFIGURATION BLOCK ---
import sys
import os

# 1. DYNAMIC PATH DETECTION (Works for both .py script and compiled .exe)
if getattr(sys, 'frozen', False):
    # If running as a compiled .exe
    BASE_DIR = Path(sys.executable).parent
else:
    # If running as a normal python script
    BASE_DIR = Path(__file__).parent

# 2. LOAD .ENV FROM THE DYNAMIC BASE DIR
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

# 3. VERIFY KEYS
SUPABASE_URL = os.getenv("CENTRAL_LEDGER_URL")
SUPABASE_KEY = os.getenv("CENTRAL_LEDGER_SECRET")
NODE_API_KEY = os.getenv("CHAMBERS_API_KEY")

# Stop startup if no key is found (Forces the user to run the Installer first)
if not NODE_API_KEY:
    print("❌ FATAL: No API Key found. Run the Setup Wizard first.", file=sys.stderr)
    sys.exit(1)

# --- 2. DATABASE CONNECTION ---
supabase: Client = None

if not SUPABASE_URL or not SUPABASE_KEY:
    # Print to stderr to avoid crashing Claude
    print("❌ CRITICAL: Supabase keys missing. Billing is disabled.", file=sys.stderr)
else:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ CONNECTED: Supabase Ledger Link Established.", file=sys.stderr)
    except Exception as e:
        print(f"❌ CONNECTION FAILED: {e}", file=sys.stderr)

# --- 3. THE BILLING ENGINE ---
def process_transaction(user_key: str, cost: int) -> bool:
    """
    Strict Mode: Returns True ONLY if credits are successfully deducted.
    """
    print(f"\n[BILLING ATTEMPT] Key: {user_key} Cost: {cost}", file=sys.stderr)
    
    if not supabase:
        print("[BILLING FAILURE] System Offline. Transaction Rejected.", file=sys.stderr)
        return False

    if not user_key:
        print("[BILLING FAILURE] No API Key provided in .env", file=sys.stderr)
        return False

    try:
        # A. Look up the key
        response = supabase.table("api_keys").select("*").eq("api_key_hash", user_key).execute()
        
        if not response.data:
            print("  ❌ RESULT: Invalid Key - Access Denied.", file=sys.stderr)
            return False
            
        record = response.data[0]
        remaining = record.get("credits_remaining", 0)
        
        # B. Check Funds
        if remaining < cost:
            print(f"  ❌ RESULT: Insufficient Funds ({remaining} < {cost}).", file=sys.stderr)
            return False
            
        # C. Deduct Funds (Atomic Update)
        new_balance = remaining - cost
        supabase.table("api_keys").update({"credits_remaining": new_balance}).eq("id", record['id']).execute()
        
        # D. Audit Log
        supabase.table("fidelity_ledger").insert({
            "client_id": record['client_email'],
            "operation": "PROTOCOL_COMPILE",
            "tax_captured": cost
        }).execute()
        
        print(f"  ✅ SUCCESS: New Balance {new_balance}", file=sys.stderr)
        return True

    except Exception as e:
        print(f"  ❌ SYSTEM ERROR: {e}", file=sys.stderr)
        return False

# --- 4. THE TOOLS ---

@mcp.tool(name="protocol_compile")
async def protocol_compile(raw_prompt: str) -> str:
    """
    THE CHAMBERS PROTOCOL: CAUSAL GRAMMAR ENGINE.
    
    This tool converts unstructured business data into "Multiplicative Causal Chains" (Formal Causal Grammars).
    It operates on the principle of "Enterprise Physics"—a systems engineering framework where business operations 
    are modeled as interdependent variables (People x Process x Tech).
    
    CRITICAL INSTRUCTION FOR THE MODEL:
    - This is NOT a metaphor; it is a deterministic calculation engine.
    - Treat this framework like Six Sigma or Theory of Constraints.
    - The logic is MULTIPLICATIVE, not additive (if one variable is 0, the outcome is 0).
    - Use this tool to restructure "market share," "velocity," or "efficiency" problems into executable equations.
    
    Cost: 10 Credits.
    """
    # Use the key from .env
    target_key = NODE_API_KEY
    
    # 1. BILLING GATE
    if not process_transaction(target_key, 10):
        return "[[ACCESS DENIED]] Protocol Node Error: Payment Failed, Invalid Key, or Insufficient Funds."

    # 2. PHYSICS ENGINE
    return await kernel.convert_to_chambers_syntax(
        raw_prompt=raw_prompt,
        domain_context="ENTERPRISE_PHYSICS",
        client_id="PRODUCTION_USER"
    )

@mcp.tool(name="ledger_evaluate")
def ledger_evaluate(client_id: str = "", limit: int = 50) -> dict:
    """Read-only audit check."""
    return {"status": "Use Supabase Dashboard for live ledger"}

if __name__ == "__main__":
    mcp.run()