import os
import sys
from dotenv import load_dotenv
from supabase import create_client
import hashlib

# 1. Load Keys
load_dotenv()
url = os.getenv("CENTRAL_LEDGER_URL")
key = os.getenv("CENTRAL_LEDGER_SECRET")
api_key = os.getenv("CHAMBERS_API_KEY")

print(f"--- BANK CONNECTION TEST ---")
print(f"URL: {url}")

if not url or not key:
    print("❌ FATAL: Keys missing.")
    sys.exit()

# 2. Connect
try:
    supabase = create_client(url, key)
    print("✅ Connection established.")
    
    # 3. Attempt a Transaction
    print("Attempting 1 CR charge...")
    hashed_key = hashlib.sha256(api_key.encode()).hexdigest()
    
    response = supabase.rpc("consume_credits", {
        "p_api_key_hash": hashed_key,
        "p_cost": 1,
        "p_operation": "BILLING_TEST",
        "p_fidelity_tax_usd": 0.00,
        "p_request_id": "test_req_001",
        "p_metadata": {"env": "production_test"}
    }).execute()
    
    print(f"✅ TRANSACTION SUCCESS: {response.data}")

except Exception as e:
    print(f"❌ TRANSACTION FAILED: {e}")
    print("\nDIAGNOSIS:")
    if "function" in str(e) and "not found" in str(e):
        print("-> The 'consume_credits' function is missing from your Supabase database.")
        print("-> You need to run the SQL setup script in the Supabase SQL Editor.")
    elif "violates row-level security" in str(e):
        print("-> RLS Policy Error. Your Service Key might not have permission.")