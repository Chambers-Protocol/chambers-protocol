import sys
print(f"python_exe: {sys.executable}")

print("\n--- 1. TESTING LIBRARIES ---")
try:
    import dotenv
    print("✅ dotenv: INSTALLED")
except ImportError as e:
    print(f"❌ dotenv: MISSING ({e})")

try:
    import supabase
    print("✅ supabase: INSTALLED")
except ImportError as e:
    print(f"❌ supabase: MISSING ({e})")

try:
    from mcp.server.fastmcp import FastMCP
    print("✅ mcp: INSTALLED")
except ImportError as e:
    print(f"❌ mcp: MISSING ({e})")

print("\n--- 2. TESTING LOCAL FILES ---")
try:
    import CHAMBERS_NODE_KERNEL
    print("✅ Kernel: FOUND")
except ImportError as e:
    print(f"❌ Kernel: IMPORT FAILED ({e})")
except Exception as e:
    print(f"❌ Kernel: CRASHED ({e})")

print("\n--- TEST COMPLETE ---")