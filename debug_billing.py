import os
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

# 1. Load Environment
script_dir = Path(__file__).parent.absolute()
env_path = script_dir / '.env'
print(f"Loading .env from: {env_path}")
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("CHAMBERS_API_KEY")
URL = os.getenv("CENTRAL_LEDGER_URL")
KEY = os.getenv("CENTRAL_LEDGER_SECRET")

# 2. Check Credentials
print(f"\n--- CREDENTIAL CHECK ---")
print(f"API KEY Found: {'YES' if API_KEY else 'NO'}")
print(f"URL Found:     {'YES' if URL else 'NO'}")
print(f"Secret Found:  {'YES' if KEY else 'NO'}")

if not (API_KEY and URL and KEY):
    print("\n[!] CRITICAL: Missing Environment Variables. Check .env file.")
    exit()

# 3. Test Connection
print(f"\n--- CONNECTION CHECK ---")
try:
    supabase = create_client(URL, KEY)
    print("Supabase Client: Initialized")
except Exception as e:
    print(f"[!] CRITICAL: Failed to create client: {e}")
    exit()

# 4. Test RPC (The Toll Booth)
print(f"\n--- TOLL BOOTH TEST ---")
hashed_key = hashlib.sha256(API_KEY.encode()).hexdigest()
print(f"Testing Key Hash: {hashed_key[:10]}...")

try:
    # Attempt to spend 1 credit to verify the pipe is open
    response = supabase.rpc("consume_credits", {
        "p_api_key_hash": hashed_key,
        "p_cost": 1,
        "p_operation": "DEBUG_TEST",
        "p_fidelity_tax_usd": 0.00,
        "p_request_id": "manual_debug", 
        "p_metadata": {"source": "console"}
    }).execute()
    
    print(f"RPC Response: {response}")
    
    if response.data is True:
        print("\n[SUCCESS] The Toll Booth is OPEN. Credits were deducted.")
    else:
        print("\n[FAILURE] The Toll Booth rejected the request (Access Denied).")
        print("Possible causes: 0 Credits remaining, License Suspended, or Invalid Key.")

except Exception as e:
    print(f"\n[ERROR] RPC Call Failed completely.")
    print(f"Error Details: {e}")
    print("Hint: Does the function 'consume_credits' exist in your Supabase?")