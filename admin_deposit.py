import os
import hashlib
from dotenv import load_dotenv
from supabase import create_client

# 1. Load your specific environment variables
load_dotenv()
url = os.getenv("CENTRAL_LEDGER_URL")
key = os.getenv("CENTRAL_LEDGER_SECRET")
my_api_key = os.getenv("CHAMBERS_API_KEY")

if not url or not key or not my_api_key:
    print("❌ ERROR: Missing keys in .env")
    exit()

# 2. Hash your API key (to match how the Gateway reads it)
# The Ledger stores the SHA256 hash, not the raw key
my_hash = hashlib.sha256(my_api_key.encode()).hexdigest()

print(f"💰 INITIATING DEPOSIT FOR:")
print(f"Key Hash: {my_hash[:8]}...")

# 3. Connect to the Bank
supabase = create_client(url, key)

# 4. Execute the Deposit (Direct SQL Injection via RPC usually, or direct insert)
# Assuming a standard ledger where positive numbers are deposits
transaction = {
    "api_key_hash": my_hash,
    "cost": -100000,  # Negative cost = Positive Credit (Deposit)
    "operation": "ADMIN_GRANT",
    "metadata": {"reason": "Developer God Mode", "authorized_by": "Chris Chambers"}
}

# NOTE: If your ledger uses a 'credit' column instead of negative cost, adjust here.
# Based on standard implementations, we usually just add a row.
try:
    # We use the same function but send a negative cost to add balance
    # Or insert directly if you have permission
    data = supabase.table("ledger").insert({
        "api_key_hash": my_hash,
        "credit_amount": 1000000, # If your table separates credits/debits
        # "cost": -1000000,      # If your table uses a single column sum
        "operation": "ADMIN_GRANT",
        "metadata": {"type": "seed_funding"}
    }).execute()
    
    print("✅ SUCCESS: 1,000,000 Credits deposited.")
    print("   The system remains secure. Only YOU have these credits.")

except Exception as e:
    print(f"❌ DEPOSIT FAILED: {e}")
    print("   (Check your table structure. You may need to use 'credit_amount' vs 'cost')")