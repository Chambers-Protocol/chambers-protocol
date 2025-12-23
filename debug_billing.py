import os
import hashlib
from dotenv import load_dotenv
from supabase import create_client

# 1. Load Environment
load_dotenv()
url = os.getenv("CENTRAL_LEDGER_URL")
key = os.getenv("CENTRAL_LEDGER_SECRET")
api_key = os.getenv("CHAMBERS_API_KEY")

print(f"--- DIAGNOSTIC ---")
print(f"URL: {url}")
print(f"API KEY DETECTED: {'Yes' if api_key else 'No'}")

if not api_key:
    print("❌ ERROR: CHAMBERS_API_KEY is missing from .env")
    exit()

# 2. Connect
try:
    supabase = create_client(url, key)
    print("✅ Supabase Connected")
except Exception as e:
    print(f"❌ Supabase Connection Failed: {e}")
    exit()

# 3. Test Transaction
hashed_key = hashlib.sha256(api_key.encode()).hexdigest()
print(f"Testing Key Hash: {hashed_key[:10]}...")

try:
    response = supabase.rpc("consume_credits", {
        "p_api_key_hash": hashed_key,
        "p_cost": 1, # Test 1 credit
        "p_operation": "DEBUG_TEST",
        "p_fidelity_tax_usd": 0.00,
        "p_request_id": None, 
        "p_metadata": {"mode": "debug"}
    }).execute()
    
    print(f"✅ BILLING SUCCESS. Result: {response.data}")
except Exception as e:
    print(f"❌ BILLING FAILED. Real Error: {e}")