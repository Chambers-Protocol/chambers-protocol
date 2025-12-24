import os

def create_init_files(root_dir):
    print(f"🔧 REPAIRING PACKAGE STRUCTURE IN: {root_dir}")
    
    if not os.path.exists(root_dir):
        print(f"❌ ERROR: Directory '{root_dir}' not found.")
        return

    # Create __init__.py in the root nodes folder
    init_path = os.path.join(root_dir, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, "w") as f:
            f.write("# Chambers Physics Kernel\n")
        print(f"✅ Created: {init_path}")

    # Walk through all subfolders
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Create __init__.py in every subfolder (oil, risk, etc.)
        for dirname in dirnames:
            sub_init = os.path.join(dirpath, dirname, "__init__.py")
            if not os.path.exists(sub_init):
                with open(sub_init, "w") as f:
                    f.write("") # Empty file is enough
                print(f"✅ Created: {sub_init}")

        # VISUAL VERIFICATION: Print existing files to check for typos
        for filename in filenames:
            if filename.endswith(".py") and filename != "__init__.py":
                print(f"   📄 Found Module: {os.path.join(dirpath, filename)}")

if __name__ == "__main__":
    create_init_files("nodes")
    print("\n🚀 REPAIR COMPLETE. Try running enterprise_gateway.py now.")