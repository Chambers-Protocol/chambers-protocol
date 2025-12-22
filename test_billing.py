import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

# 1. LOAD CONFIG
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

print("--- DIAGNOSTIC START ---")

# 2. CHECK CREDENTIALS
url = os.getenv("CENTRAL_LEDGER_URL")
secret = os.getenv("CENTRAL_LEDGER_SECRET")
api_key = os.getenv("CHAMBERS_API_KEY")

if not url or not secret:
    print("❌ MISSING: URL or Secret in .env file")
    exit()

print(f"✅ URL Found: {url}")
print(f"✅ Secret Found: {secret[:10]}...")
print(f"✅ User Key: {api_key}")

# 3. TEST CONNECTION
try:
    print("\n📡 Connecting to Supabase...")
    supabase = create_client(url, secret)
    
    print("🔍 Searching for API Key in Database...")
    response = supabase.table("api_keys").select("*").eq("api_key_hash", api_key).execute()
    
    if not response.data:
        print("❌ FAILURE: Connection worked, but Key was NOT found in the database.")
        print("   -> Check for typos in the .env file vs the Supabase dashboard.")
    else:
        user = response.data[0]
        print(f"✅ SUCCESS! Found User: {user.get('client_email')}")
        print(f"💰 Current Balance: {user.get('credits_remaining')}")
        
        # 4. TEST DEDUCTION (Optional)
        print("\n🧪 Attempting Test Deduction (1 Credit)...")
        new_balance = user.get('credits_remaining') - 1
        supabase.table("api_keys").update({"credits_remaining": new_balance}).eq("id", user['id']).execute()
        print(f"✅ DEDUCTION WORKED! New Balance: {new_balance}")

except Exception as e:
    print("\n🔥 CRITICAL FAILURE 🔥")
    print(f"Error Details: {e}")

print("--- DIAGNOSTIC END ---")