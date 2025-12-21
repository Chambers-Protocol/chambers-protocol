import os
from pathlib import Path
from dotenv import load_dotenv

# 1. Check where we are
current_dir = Path.cwd()
script_dir = Path(__file__).parent
print(f"📍 DIRECTORY CHECK:")
print(f"   Run from: {current_dir}")
print(f"   Script at: {script_dir}")

# 2. Hunt for the .env file
target_env = script_dir / ".env"
print(f"\n🔍 LOOKING FOR .env FILE:")
print(f"   Checking: {target_env}")

if target_env.exists():
    print(f"   ✅ FOUND IT! The file exists.")
    
    # 3. Test Loading
    load_dotenv(target_env)
    secret = os.getenv("CENTRAL_LEDGER_SECRET")
    api_key = os.getenv("CHAMBERS_API_KEY")

    print(f"\n🔑 KEY CHECK:")
    if secret:
        if secret.startswith("eyJ"):
             print(f"   ✅ Ledger Secret: VALID (Starts with {secret[:5]}...)")
        else:
             print(f"   ❌ Ledger Secret: INVALID FORMAT (Starts with {secret[:5]}...) -> Must be 'eyJ...'")
    else:
        print(f"   ❌ Ledger Secret: MISSING from file.")

    if api_key:
        print(f"   ✅ User API Key:  FOUND ({api_key[:10]}...)")
    else:
        print(f"   ❌ User API Key:  MISSING.")
        
else:
    print(f"   ❌ ERROR: .env file NOT found.")
    print(f"   Files actually in this folder:")
    for f in script_dir.iterdir():
        if f.is_file():
            print(f"    - {f.name}")