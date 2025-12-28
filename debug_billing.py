import os
import sys
import json
import hashlib
from dotenv import load_dotenv
from supabase import create_client

# 1. Setup
load_dotenv()
url = os.getenv("CENTRAL_LEDGER_URL")
key = os.getenv("CENTRAL_LEDGER_SECRET")
api_key = os.getenv("CHAMBERS_API_KEY")

print("--- BILLING DIAGNOSTICS ---")

if not url or not key or not api_key:
    print("❌ KEYS MISSING")
    sys.exit()

# 2. Hash the key (Same logic as Gateway)
hashed_key = hashlib.sha256(api_key.encode()).hexdigest()
print(f"🔑 Key Hash: {hashed_key[:8]}...")

# 3. Connect
try:
    supabase = create_client(url, key)
    print("✅ Connected to Supabase.")
except Exception as e:
    print(f"❌ Connection Failed: {e}")
    sys.exit()

# 4. Attempt the RPC Call (Exact same parameters as Gateway)
print("\n💸 Attempting 'consume_credits' RPC call...")
params = {
    "p_api_key_hash": hashed_key,
    "p_cost": 1,
    "p_operation": "DEBUG_TEST",
    "p_fidelity_tax_usd": 0.00,
    "p_request_id": "debug_001",
    "p_metadata": {"env": "test"}
}

try:
    response = supabase.rpc("consume_credits", params).execute()
    print(f"✅ SUCCESS! Result: {response.data}")
    print("(If this says True, your billing is fixed. If False, check balance.)")
except Exception as e:
    print(f"\n❌ RPC FAILED. RAW ERROR:")
    print(f"{str(e)}")
    
    # 5. Analysis
    err = str(e)
    if "function" in err and "does not exist" in err:
        print("\n🔎 DIAGNOSIS: Schema Cache Stale or Function Signature Mismatch.")
        print("   -> Go to Supabase Dashboard > API Docs.")
        print("   -> This often forces a schema refresh.")
    elif "violates" in err:
        print("\n🔎 DIAGNOSIS: RLS or Constraint Violation.")
    elif "argument" in err:
        print("\n🔎 DIAGNOSIS: Parameter Name Mismatch.")
        print("   The Python dict keys must match the SQL function arguments exactly.")