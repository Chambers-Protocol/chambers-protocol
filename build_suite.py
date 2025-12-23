import PyInstaller.__main__
import os

print("🚧 BUILDING CHAMBERS ENTERPRISE SUITE...")

PyInstaller.__main__.run([
    'enterprise_grid.py',                # Main Script
    '--name=ChambersEnterpriseGrid',     # EXE Name
    '--onefile',                         # Single EXE
    '--clean',
    '--add-data=nodes;nodes',            # Include the Nodes folder
    '--hidden-import=decimal',           # Critical for math
    '--hidden-import=json',
    '--collect-all=mcp',                 # Ensure MCP library is packed
    '--collect-all=supabase'             # Ensure Supabase is packed
])

print("✅ BUILD COMPLETE. Check the /dist folder.")