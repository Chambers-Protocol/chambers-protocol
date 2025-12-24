import os
import re

def scan_classes(root_dir="nodes"):
    print(f"🔦 X-RAY SCANNING: {root_dir}...\n")
    
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith("_kernel.py"):
                path = os.path.join(dirpath, filename)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Find lines starting with 'class '
                    matches = re.findall(r"^class\s+(\w+)", content, re.MULTILINE)
                    
                    if matches:
                        rel_path = os.path.relpath(path, root_dir)
                        # Format: nodes.oil.oil_kernel -> ClassName
                        print(f"📄 {rel_path}")
                        for m in matches:
                            print(f"   └── 📦 CLASS: {m}")
                        print("")

if __name__ == "__main__":
    scan_classes()