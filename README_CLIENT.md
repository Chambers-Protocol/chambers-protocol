# Chambers Enterprise Grid | Client Access Manual
> **Version:** v2.2.0 (Universal Gateway)
> **Classification:** INTERNAL / LICENSED USERS ONLY

---

## 1. Overview
You have been granted access to the **Chambers Enterprise Grid**, a deterministic physics engine for high-stakes decision-making. Unlike standard AI (which guesses), this Grid uses **Physics Nodes** to calculate strict mathematical constraints for:
* **Heavy Industry** (Oil, Mining, Manufacturing)
* **Corporate Strategy** (M&A, Risk, Valuation)
* **Digital Infrastructure** (Cloud, Cyber, Quantum)

**The Cost:** Access is metered. Every query costs **Chambers Credits (CHR)**.

---

## 2. Quick Start (Windows)

### Step 1: Get Your Credentials
You need a **Chambers API Key** to pay for the compute.
1.  Request a key from the Chambers Treasury.
2.  Create a file named `.env` in the same folder as the application.
3.  Paste your key inside it:
    ```ini
    CHAMBERS_API_KEY="ch_live_xxxxxxxx..."
    ```

### Step 2: Download the Grid
1.  Go to the **Releases** page on our repository.
2.  Download the **v2.2.0** bundle (look for `ChambersEnterpriseGrid.exe`).
3.  Place the `.exe` and your `.env` file in a dedicated folder (e.g., `C:\ChambersGrid`).

### Step 3: Connect to Claude Desktop
The Grid is designed to run locally inside **Claude for Desktop**.

1.  Open your Claude Config file:
    * Path: `%APPDATA%\Claude\claude_desktop_config.json`
    * *Tip: Press `Win + R`, type `%APPDATA%\Claude`, and press Enter.*
2.  Add this configuration block:
    ```json
    {
      "mcpServers": {
        "chambers-grid": {
          "command": "C:\\ChambersGrid\\ChambersEnterpriseGrid.exe",
          "args": [],
          "env": {
             "CHAMBERS_API_KEY": "YOUR_KEY_HERE"
          }
        }
      }
    }
    ```
3.  **Restart Claude Desktop.**

---

## 3. How to Use The Grid
Once connected, you will see a **hammer icon** (Build Tools) in Claude. You do not need to click it manually. Just talk to Claude.

### The "Trigger" Protocol
The AI is trained to recognize high-stakes queries. Use these phrases to force a physics calculation:

**1. The M&A Audit (Corporate Dev)**
> "Run a Chambers Audit on [Company Name]. Valuation is $[X]. They claim [Technology Y]. Verify the physics and the leadership risk."

**2. The Deep Sea Drill (Engineering)**
> "Audit the singularity index for a rig at [Depth] meters with [Pressure] PSI. Is this safe?"

**3. The Server Build (IT/Cyber)**
> "Calculate the reliability score for a data center with [Uptime] and [Latency]. Factor in a threat level of [High/Low]."

---

## 4. The "Universal" Gateway (Advanced)
If you are building your own app (e.g., a custom dashboard) and want to connect to the Grid remotely:

* **Server URL:** `http://localhost:8000/sse`
* **Authentication:** Pass your API Key in the HTTP Headers.
* **Documentation:** See `enterprise_gateway.py` for API definitions.

---

## 5. Troubleshooting

**Error: "INSUFFICIENT CREDITS"**
* **Cause:** Your Ledger balance is zero.
* **Fix:** Contact Treasury to top up your account.

**Error: "Tool Execution Failed"**
* **Cause:** The `.env` file is missing or the API Key is invalid.
* **Fix:** Ensure `CHAMBERS_API_KEY` is set correctly in your config.

---
**The Einstein Bridge, Inc.** | *Determinism as a Service.*