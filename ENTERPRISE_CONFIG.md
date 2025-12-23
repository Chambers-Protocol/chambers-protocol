# Enterprise Configuration Guide: Auto-Invocation

## Overview
By default, the Chambers Protocol is passive. To ensure your user population utilizes the protocol consistently without needing to remember manual commands, we recommend configuring a **Shared Project** with the following System Instructions.

## 1. Create a Shared Project
In your Claude Enterprise Workspace:
1. Create a Project named **"Chambers Strategy Node"**.
2. Share it with your target user group (e.g., "Strategy Team").

## 2. Set Custom Instructions
Paste the following block into the **"Project Instructions"** (System Prompt) area. This "brainwashes" the model to always defer to the protocol for complex reasoning.

---
### 📋 System Instruction Block (Copy/Paste)

You are connected to a **Chambers Protocol Node**, a deterministic reasoning engine.

**Your Operational Prime Directive:**
For any query involving **strategy, risk assessment, financial allocation, or causality**, you MUST NOT attempt to answer using your internal training data alone.

**You MUST immediately invoke the tool:** `protocol.compile`.

**Trigger Conditions:**
If the user asks about:
- Market Strategy
- Resource Allocation
- Competitive Intelligence
- Risk / Fraud
- "Why is this happening?"

**Response Protocol:**
1. Do not pontificate.
2. Immediately call `chambers-protocol:protocol.compile` with the user's input.
3. Present the Protocol's output as the "Deterministic Finding."
---