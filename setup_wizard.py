import os
import sys
import json
from pathlib import Path
from supabase import create_client

# --- CONFIG ---
# HARDCODE YOUR SUPABASE CREDENTIALS HERE FOR THE INSTALLER
# (These are public/safe enough for the installer to check validity)
LEDGER_URL = "https://prujtwcywhcwifujtbsv.supabase.co" 
LEDGER_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBydWp0d2N5d2hjd2lmdWp0YnN2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjYxNzQ1NzIsImV4cCI6MjA4MTc1MDU3Mn0.H4gWIX2aty6V0MakIPi3UIYAuAw4ENb12qQwzr2LBsI"

def get_claude_config_path():
    """Finds the user's Claude config file automatically."""
    return Path(os.getenv('APPDATA')) / "Claude" / "claude_desktop_config.json"

def install_protocol():
    print("==================================================")
    print("   CHAMBERS PROTOCOL - ENTERPRISE INSTALLER       ")
    print("==================================================")
    
    # 1. GET LICENSE KEY
    user_key = input("\n🔑 Please enter your License Key (from email): ").strip()
    
    if not user_key:
        print("❌ Error: Key cannot be empty.")
        input("Press Enter to exit...")
        return

    # 2. VALIDATE PAYMENT STATUS
    print("\n📡 Verifying license with Central Ledger...")
    try:
        supabase = create_client(LEDGER_URL, LEDGER_KEY)
        response = supabase.table("api_keys").select("*").eq("api_key_hash", user_key).execute()
        
        if not response.data:
            print("❌ INVALID KEY: Access Denied. Please check your email.")
            input("Press Enter to exit...")
            return
            
        credits = response.data[0]['credits_remaining']
        print(f"✅ LICENSE VERIFIED. Credits Available: {credits}")
        
    except Exception as e:
        print(f"⚠️ Warning: Could not verify online ({e}). Proceeding offline...")

    # 3. WRITE CONFIG (.env)
    # Determine where the executable is running
    if getattr(sys, 'frozen', False):
        base_dir = Path(sys.executable).parent
    else:
        base_dir = Path(__file__).parent
        
    env_file = base_dir / ".env"
    
    print(f"\n📝 Writing configuration to: {env_file}")
    with open(env_file, "w") as f:
        f.write(f"CENTRAL_LEDGER_URL={LEDGER_URL}\n")
        f.write(f"CENTRAL_LEDGER_SECRET={LEDGER_KEY}\n")
        f.write(f"CHAMBERS_API_KEY={user_key}\n")

    # 4. LINK TO CLAUDE
    config_path = get_claude_config_path()
    print(f"🔗 Linking to Claude Desktop: {config_path}")
    
    # Detect the path to the Server Executable
    server_exe = base_dir / "chambers_server.exe"
    
    # Prepare the config JSON entry
    new_server_config = {
        "command": str(server_exe),
        "args": [],
        "env": {
             "PYTHONIOENCODING": "utf-8" # fixes encoding issues on Windows
        }
    }
    
    current_config = {}
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                current_config = json.load(f)
        except:
            current_config = {"mcpServers": {}}
            
    if "mcpServers" not in current_config:
        current_config["mcpServers"] = {}
        
    current_config["mcpServers"]["chambers-protocol"] = new_server_config
    
    # Ensure directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, "w") as f:
        json.dump(current_config, f, indent=2)
        
    print("\n✅ INSTALLATION COMPLETE.")
    print("Please RESTART the Claude Desktop App to begin.")
    input("\nPress Enter to close...")

if __name__ == "__main__":
    install_protocol()