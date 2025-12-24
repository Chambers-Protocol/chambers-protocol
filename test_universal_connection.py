import requests
import json

# The Universal Port you just opened
URL = "http://127.0.0.1:8000/sse"

print(f"📡 PINGING CHAMBERS GATEWAY AT: {URL} ...")

try:
    # We attempt to shake hands with the server
    response = requests.get(URL, stream=True, timeout=5)
    
    if response.status_code == 200:
        print("✅ CONNECTION ESTABLISHED: 200 OK")
        print("💎 The Grid is broadcasting. Any AI can now listen.")
        
        # Verify it identifies itself correctly
        print("\n--- SERVER HEADERS ---")
        for k, v in response.headers.items():
            print(f"{k}: {v}")
    else:
        print(f"❌ CONNECTION FAILED: {response.status_code}")

except Exception as e:
    print(f"❌ ERROR: {e}")
    print("Ensure 'enterprise_gateway.py' is running in a separate window!")