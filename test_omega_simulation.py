import requests

# The Omega Port
URL = "http://127.0.0.1:9000/sse"

print(f"🔭 CONNECTING TO CHAMBERS X (OMEGA) AT: {URL} ...")

try:
    # Ping the Server to see if it is alive
    response = requests.get(URL, stream=True, timeout=5)
    
    if response.status_code == 200:
        print("✅ CONNECTION ESTABLISHED: 200 OK")
        print("🌌 The Omega Protocol is active.")
        print("\n--- SERVER HEADERS ---")
        for k, v in response.headers.items():
            print(f"{k}: {v}")
    else:
        print(f"❌ CONNECTION FAILED: {response.status_code}")

except Exception as e:
    print(f"❌ ERROR: {e}")
    print("Ensure 'omega_gateway.py' is running on Port 9000!")