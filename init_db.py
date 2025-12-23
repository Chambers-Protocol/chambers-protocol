import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
url = os.getenv("CENTRAL_LEDGER_URL")
key = os.getenv("CENTRAL_LEDGER_SECRET")

supabase = create_client(url, key)

print("--- INITIALIZING CHAMBERS DATABASE ---")

# SQL to create the missing tables
sql_licenses = """
create table if not exists licenses (
  id uuid default gen_random_uuid() primary key,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  email text not null,
  api_key_hash text not null unique,
  credits_balance integer default 0,
  tier text default 'STANDARD'
);
"""

sql_ledger = """
create table if not exists ledger (
  id uuid default gen_random_uuid() primary key,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  license_id uuid references licenses(id),
  operation text not null,
  cost integer not null,
  metadata jsonb
);
"""

# The Function to handle billing safely
sql_function = """
create or replace function consume_credits(
  p_api_key_hash text,
  p_cost int,
  p_operation text,
  p_fidelity_tax_usd numeric,
  p_request_id text,
  p_metadata jsonb
)
returns boolean
language plpgsql
security definer
as $$
declare
  v_license_id uuid;
  v_current_balance int;
begin
  -- 1. Check if License Exists & Lock Row
  select id, credits_balance into v_license_id, v_current_balance
  from licenses
  where api_key_hash = p_api_key_hash
  for update;

  if v_license_id is null then
    raise exception 'INVALID_KEY_OR_INSUFFICIENT_CREDITS';
  end if;

  -- 2. Check Balance
  if v_current_balance < p_cost then
    raise exception 'INVALID_KEY_OR_INSUFFICIENT_CREDITS';
  end if;

  -- 3. Deduct Credits
  update licenses
  set credits_balance = credits_balance - p_cost
  where id = v_license_id;

  -- 4. Write to Ledger
  insert into ledger (license_id, operation, cost, metadata)
  values (v_license_id, p_operation, p_cost, p_metadata);

  return true;
end;
$$;
"""

try:
    print("1. Creating 'licenses' table...")
    supabase.rpc("exec_sql", {"query": sql_licenses}).execute() 
    # NOTE: If exec_sql isn't enabled on your Supabase (it's rare), 
    # this script might fail. If so, you have to paste the SQL into the dashboard.
    # But usually, the "consume_credits" function is what we really need, 
    # and we can try to install it via standard query if possible, 
    # or we guide you to the dashboard.
    
    # Actually, standard Supabase-py clients can't run raw DDL (CREATE TABLE) 
    # without a special Postgres connection or the Dashboard SQL Editor.
    
    print("⚠️  STOP. I cannot create tables from Python directly due to security permissions.")
    print("You must paste the SQL code into the Supabase Dashboard.")
    
except Exception as e:
    print(f"Check: {e}")

print("\n--- INSTRUCTIONS ---")
print("1. Log in to https://supabase.com/dashboard")
print("2. Open your Project.")
print("3. Click 'SQL Editor' (on the left sidebar).")
print("4. Click 'New Query'.")
print("5. Paste the code below and run it:")
print("-" * 30)
print(sql_licenses)
print(sql_ledger)
print(sql_function)
print("-" * 30)