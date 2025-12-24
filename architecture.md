# Chambers Enterprise Grid: Architecture Reference

> **System Version:** v2.1.0 (Gold Master)  
> **Architecture Type:** Hybrid Probabilistic-Deterministic Cognitive Engine  
> **Protocol:** Model Context Protocol (MCP) via Local Pipe  

---

## 1. High-Level System Overview

The **Chambers Enterprise Grid** serves as a "Reasoning Governor" for Large Language Models. It solves the hallucination problem by intercepting specific queries and routing them through immutable, deterministic algorithms (written in Python) before returning a response to the AI.

### The "Hard Physics" Topology
Instead of allowing the AI to guess, the Grid forces it to invoke a tool.

```mermaid
graph TD
    User[User / Executive] -->|Prompt| Claude[Claude Desktop App]
    Claude -->|MCP JSON-RPC| Grid[Enterprise Grid Controller]
    
    subgraph "The Physics Constellation"
        Grid -->|Route| Node1[Risk Node]
        Grid -->|Route| Node2[Oil & Gas Node]
        Grid -->|Route| Node3[Venture Node]
        Grid -->|Route| Node4[Cloud Ops Node]
        Grid -->|Route| Node5[Cyber Node]
        Grid -->|Route| Node6[Thermo Node]
        Grid -->|Route| Node7[Semiconductor Node]
        Grid -->|Route| Node8[Product Node]
        Grid -->|Route| Node9[Cognitive Node]
        Grid -->|Route| Node10[Research Node]
    end
    
    subgraph "The Central Ledger"
        Grid -->|Auth & Bill| Supabase[(Supabase DB)]
        Supabase -->|Confirm| Grid
    end
    
    Node1 & Node2 & Node3 & Node4 & Node5 & Node6 & Node7 & Node8 & Node9 & Node10 -->|Calculated Data| Grid
    Grid -->|Deterministic Result| Claude
    Claude -->|Synthesized Answer| User

---

2. Component Breakdown

A. The Grid Controller (enterprise_grid.py)

Role: The Orchestrator.

Function: Monolithic Server running on Port 8000 (standard IO pipe). It imports all 10 kernels and exposes them as distinct tools to the MCP client.

Key Feature: Implements sys.stderr logging to prevent stdout pollution, ensuring stable connections with Claude.

B. The Physics Kernels (nodes/)

Independent, logic-pure Python classes that contain the "Chambers Framework" math. They have zero dependencies on the outside world (no API calls, no AI). They simply compute inputs into outputs based on strict formulas.

Node,Domain,Core Mechanic
Risk Mechanics,Finance/Compliance,Multiplicative Failure Modeling  Failure = Risk_A * Risk_B
Oil & Gas,Heavy Industry,Singularity Index  (Drilling * Geology) / Safety
Venture,M&A / PE,Valuation Velocity  Team * Market * Product * Time
Cloud Ops,Infrastructure,Reliability Engineering  Uptime * Latency * Cost
Cybersecurity,InfoSec,Defense-in-Depth Score  (Posture - Threat) * Resilience
Thermoelectric,Energy Science,Efficiency Conversion  Seebeck_Coeff * Temp_Diff
Semiconductor,Manufacturing,Yield Sustainability  Lithography * Purity * Eco_Cost
Product,Strategy,Pipeline Probability  (Strategy + Exec) * Speed
Cognitive,Psychology,Decision Framework  (Hardware * Software) - Bias
Research,R&D,HPQAI Convergence  Quantum * AI * HPC

C. The Central Ledger (Supabase)

Role: The "bank" and the "auditor."

Billing Logic: Uses a stored procedure (consume_credits) to execute Atomic Transactions.

Hashes the User's API Key (SHA-256).

Locks the license row.

Checks balance > Cost.

Deducts credits.

Writes to the immutable ledger table.

Returns TRUE.

Security: The API Key is never stored in plain text in the database.

---

3. Data Flow & Security

1. The Invocation
The user asks: "Audit the risk of Project X." Claude recognizes the intent and constructs a JSON payload:

{ 
  "tool": "risk_audit", 
  "args": { "alpha_integrity": 0.8, "defense_score": 0.9 } 
}

2. The Verification

The Grid Controller receives the JSON.

Step 1: Extracts CHAMBERS_API_KEY from local env.

Step 2: Pings Supabase to pay "Computation Tax."

Step 3: If Billing Fails ➔ Returns "⛔ Insufficient Credits".

Step 4: If Billing Succeeds ➔ Passes data to RiskMechanicsEngine.

3. The Computation

The RiskMechanicsEngine executes the math.

It does not hallucinate.

If 0.8 * 0.8 = 0.64, it will always return 0.64.

4. The Synthesis

Claude receives the raw number (0.64) and uses language capabilities to explain the strategic implication of that number.

---

4. Deployment Model

The system is compiled into a "Frozen Binary" using PyInstaller.

Artifact: ChambersEnterpriseGrid.exe

Distribution: Single file + .env config.

Requirements: None. The client does not need Python, Pip, or Docker. The executable contains the Python interpreter and all libraries (Pydantic, Supabase, etc.) bundled inside.

---

5. Directory Structure

chambers-protocol/
├── enterprise_grid.py       # MAIN ENTRY POINT (The Controller)
├── build_suite.py           # The Compiler Script
├── mint_license.py          # Admin Tool (Generate Keys)
├── fix_database.py          # Admin Tool (Repair DB Sync)
├── .env                     # Secrets (Not in Git)
├── nodes/                   # The Physics Kernels
│   ├── risk/
│   ├── oil/
│   ├── venture/
│   └── ... (10 total)
└── dist/                    # The Output Folder
    └── ChambersEnterpriseGrid.exe  # THE PRODUCT