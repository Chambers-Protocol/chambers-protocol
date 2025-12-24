import os
import time
import sys
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client

# 1. Connect to the Bank
load_dotenv()
url = os.getenv("CENTRAL_LEDGER_URL")
key = os.getenv("CENTRAL_LEDGER_SECRET") # Must use SERVICE_ROLE key for full access
supabase = create_client(url, key)

EXCHANGE_RATE = 0.01 # $0.01 per Credit

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_ledger_stats():
    # Fetch total transactions
    ledger_count = supabase.table("ledger").select("*", count="exact").execute()
    total_tx = ledger_count.count
    
    # Fetch total credits burned (Revenue)
    # Note: efficient sum requires a DB function, but for now we pull data
    # For speed in Python, we might limit this or sum strictly new ones
    # but let's grab the last 1000 to estimate or all if small.
    # PRO TIP: In production, write a SQL function 'get_total_revenue()'
    all_tx = supabase.table("ledger").select("cost").execute()
    total_credits = sum(record['cost'] for record in all_tx.data)
    
    # Fetch recent logs
    recent = supabase.table("ledger").select("*").order("created_at", desc=True).limit(8).execute()
    
    return total_tx, total_credits, recent.data

def render_dashboard():
    while True:
        try:
            total_tx, total_credits, recent_logs = get_ledger_stats()
            revenue_usd = total_credits * EXCHANGE_RATE
            
            clear_screen()
            print("💎 CHAMBERS ENTERPRISE GRID | REAL-TIME TREASURY 💎")
            print("=" * 60)
            print(f"💰 GROSS REVENUE:      ${revenue_usd:,.2f}")
            print(f"🧾 TOTAL TRANSACTIONS: {total_tx:,}")
            print(f"🔥 CREDITS BURNED:     {total_credits:,}")
            print("-" * 60)
            print("LIVE TRANSACTION FEED:")
            print(f"{'TIMESTAMP':<25} | {'NODE / OPERATION':<30} | {'COST':<5}")
            print("-" * 60)
            
            for log in recent_logs:
                ts = log['created_at'].split('.')[0].replace('T', ' ')
                op = log['operation'][:28]
                cost = log['cost']
                print(f"{ts:<25} | {op:<30} | {cost} CR")
                
            print("=" * 60)
            print(f"Last Update: {datetime.now().strftime('%H:%M:%S')} (Polling...)")
            
            time.sleep(3) # Refresh rate
            
        except KeyboardInterrupt:
            print("\n🛑 Dashboard Closed.")
            sys.exit()
        except Exception as e:
            print(f"Connection Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    print("Connecting to Central Ledger...")
    render_dashboard()