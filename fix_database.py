import os
import hashlib
from dotenv import load_dotenv
from supabase import create_client

# 1. Load the Key you already have
load_dotenv()
url = os.getenv("CENTRAL_LEDGER_URL")
secret = os.getenv("CENTRAL_LEDGER_SECRET")
my_key = os.getenv("CHAMBERS_API_KEY")

if not my_key:
    print("❌ Error: No API Key found in .env file.")
    exit()

# 2. Connect to Database
supabase = create_client(url, secret)

# 3. Calculate the Correct Hash
# This is the "Lock" that matches your "Key"
correct_hash = hashlib.sha256(my_key.encode()).hexdigest()

print(f"--- FIXING DATABASE LICENSE ---")
print(f"Key in .env: {my_key[:15]}...")
print(f"Target Hash: {correct_hash[:15]}...")

try:
    # 4. Force Insert/Update the Record
    # We use 'upsert' to overwrite any broken record with this email
    data = {
        "email": "admin_override@chambers.com", # Using a unique admin email
        "api_key_hash": correct_hash,           # The vital part
        "credits_balance": 1000000,             # Infinite money
        "tier": "ENTERPRISE_MASTER"
    }
    
    response = supabase.table("licenses").upsert(data, on_conflict="api_key_hash").execute()
    
    print("\n✅ SUCCESS: Database updated manually.")
    print("The Lock (Database) now perfectly matches your Key (.env).")
    
except Exception as e:
    print(f"\n❌ FAILED: {e}")