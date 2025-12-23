import PyInstaller.__main__
import os
import shutil

print("🚧 CLEANING PREVIOUS BUILDS...")
if os.path.exists("dist"): shutil.rmtree("dist")
if os.path.exists("build"): shutil.rmtree("build")

print("🚧 BUILDING CHAMBERS ENTERPRISE SUITE...")

PyInstaller.__main__.run([
    'enterprise_grid.py',                # Main Script
    '--name=ChambersEnterpriseGrid',     # EXE Name
    '--onefile',                         # Single EXE file
    '--clean',                           # Clean cache
    '--add-data=nodes;nodes',            # Include the Physics Kernels
    '--hidden-import=decimal',           # Math libraries
    '--hidden-import=json',
    '--hidden-import=dotenv',            # Environment variables
    '--collect-all=mcp',                 # Pack the MCP Server
    '--collect-all=supabase',            # Pack the Database Client
    '--collect-all=postgrest',           # Supabase Dependency
    '--collect-all=gotrue',              # Supabase Auth Dependency
    '--collect-all=pydantic'             # Data validation
])

print("\n✅ BUILD COMPLETE. Your artifact is in the /dist folder.")