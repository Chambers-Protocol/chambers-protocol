import os
import threading
import time
import hashlib
from dotenv import load_dotenv
from supabase import create_client

# 1. Setup
load_dotenv()
url = os.getenv("CENTRAL_LEDGER_URL")
key = os.getenv("CENTRAL_LEDGER_SECRET")
api_key = os.getenv("CHAMBERS_API_KEY")

if not api_key:
    print("❌ Error: No API Key found.")
    exit()

supabase = create_client(url, key)
hashed_key = hashlib.sha256(api_key.encode()).hexdigest()

# 2. Get Starting Balance
def get_balance():
    response = supabase.table("licenses").select("credits_balance").eq("api_key_hash", hashed_key).execute()
    return response.data[0]["credits_balance"]

start_balance = get_balance()
print(f"🏦 STARTING BALANCE: {start_balance}")

# 3. The Attack Function
COST_PER_CALL = 10
THREADS = 50
success_count = 0
fail_count = 0
lock = threading.Lock()

def spam_the_ledger(thread_id):
    global success_count, fail_count
    try:
        # Hitting the database as fast as possible
        supabase.rpc("consume_credits", {
            "p_api_key_hash": hashed_key,
            "p_cost": COST_PER_CALL,
            "p_operation": "STRESS_TEST",
            "p_fidelity_tax_usd": 0.00,
            "p_request_id": f"thread_{thread_id}", 
            "p_metadata": {"mode": "attack"}
        }).execute()
        
        with lock:
            print(f"✅ Thread {thread_id}: PAID")
            success_count += 1
    except Exception as e:
        with lock:
            print(f"❌ Thread {thread_id}: DENIED ({e})")
            fail_count += 1

# 4. Launch the Swarm
print(f"\n🚀 LAUNCHING {THREADS} CONCURRENT AGENTS...")
print(f"Expected Cost: {THREADS * COST_PER_CALL} credits")
start_time = time.time()

threads = []
for i in range(THREADS):
    t = threading.Thread(target=spam_the_ledger, args=(i,))
    threads.append(t)
    t.start()

# Wait for all to finish
for t in threads:
    t.join()

end_time = time.time()
duration = end_time - start_time

# 5. The Audit
print("\n--- AUDIT RESULTS ---")
print(f"Time Taken: {duration:.2f} seconds")
print(f"Successful Tolls: {success_count}")
print(f"Failed Tolls:     {fail_count}")

final_balance = get_balance()
expected_balance = start_balance - (success_count * COST_PER_CALL)

print(f"\nExpected Balance: {expected_balance}")
print(f"Actual Balance:   {final_balance}")

if final_balance == expected_balance:
    print("\n💎 INTEGRITY CONFIRMED. ZERO LEAKAGE.")
    print("The Row-Locking prevented all race conditions.")
else:
    print("\n💀 CRITICAL FAILURE. MONEY WAS LOST/GAINED.")
    print(f"Discrepancy: {final_balance - expected_balance}")