# Chambers Protocol
**Deterministic Reasoning Infrastructure for Entropy-Bound Systems**

![License](https://img.shields.io/badge/License-Enterprise-blue)
![Billing](https://img.shields.io/badge/Billing-Atomic-green)
![Ledger](https://img.shields.io/badge/Ledger-Append--Only-blue)
![Status](https://img.shields.io/badge/Status-Production-black)

---

## 💎 Licensing & Access Tiers

The Chambers Protocol is an enterprise-grade cognitive infrastructure layer. Access is controlled via provisioned **Protocol Nodes**, which are licensed based on organizational scale rather than seat count.

We offer three tiers of node deployment:

| Tier | Scale | Usage Model | Access Method |
| :--- | :--- | :--- | :--- |
| **Pilot Node** | Single Team (5-20 Users) | 1,000,000 Credit Allocation | [**Purchase License via Stripe ($1,000)**](https://buy.stripe.com/6oUeVf0Nv61GgWR5i81kA00) |
| **Divisional Node** | Department (50-500 Users) | Annual High-Volume License | [**Contact Research Team**](mailto:Research@theeinsteinbridge.com) |
| **Enterprise Grid** | Global (Unlimited Users) | Unrestricted / Custom SLA | [**Contact Research Team**](mailto:Research@theeinsteinbridge.com) |

### 🔐 Provisioning Process

**For Pilot Nodes (Self-Serve):**
1. Complete the secure checkout via the Stripe link above.
2. Your **License Key** will be automatically minted and delivered to your billing email.
3. Download the **Enterprise Installer** linked in your welcome email.

**For Divisional & Enterprise Grids:**
Please contact `Research@theeinsteinbridge.com` to initiate a deployment audit.
* Volume licensing agreements are available for annual terms.
* Enterprise Nodes support silent deployment (SCCM/Intune) and custom security policies.

---

## Overview

Chambers Protocol is a mechanically enforced reasoning and billing layer operating at the boundary between **human input** and **machine computation**.

It exists to address a hard constraint:

- Unbounded language generates entropy
- Entropy generates heat
- Heat limits computation

Chambers Protocol constrains this process by enforcing **deterministic transformation**, **atomic accounting**, and **auditable cost surfaces** at the moment computation is invoked.

This repository hosts the **production MCP Server implementation**.

Formal system guarantees and tester validation are documented in VERIFICATION.md.

---

## What This Is (Precisely)

Chambers Protocol is:

- A **Model Context Protocol (MCP) Server**
- A **deterministic transform gate** between user input and model execution
- A **credit-metered, entropy-bounded compute interface**
- A **write-once, auditable fidelity ledger**

It is **not**:

- a chatbot
- a prompt library
- a UX product
- an AI assistant

It is infrastructure.

---

## Core Principle

**Entropy must be paid for.**

Every invocation of the protocol:

- consumes a fixed amount of credits
- generates a fixed fidelity tax
- is recorded in an append-only ledger
- executes **only after atomic verification**

No heuristics.
No retries.
No silent failures.

---

## Deterministic Billing Model

Billing is enforced **before computation**.

Mechanism:

1. API key is hashed deterministically (SHA-256)
2. Credits are decremented via a **single atomic database operation**
3. Failure halts execution
4. Success permits protocol execution
5. A ledger entry is appended (non-blocking, write-once)

There is no read-then-write race condition.

---

## Fidelity Ledger (Audit Guarantees)

All protocol executions are recorded in a **write-once audit table**.

### Ledger Properties

- Append-only  
- Timestamped  
- Immutable  
- Deterministic  
- Human-auditable  
- Machine-verifiable  

### Canonical Ledger Fields

- `created_at`  
- `client_email`  
- `api_key_hash`  
- `operation`  
- `credits_cost`  
- `fidelity_tax_usd`  
- `request_id`  
- `metadata`  

Ledger writes are best-effort and non-blocking.  
Execution **never depends on audit success**.

---

## Mechanical Guarantees

The system guarantees:

- Atomic credit consumption  
- Deterministic hashing  
- No floating state  
- No silent degradation  
- No anthropomorphic interpretation layer  
- Explicit failure modes  

If a request executes, it was paid for.  
If it was not paid for, it does not execute.

---

### Explicit Invocation Guarantee

Chambers Protocol never executes implicitly.

- No background monitoring
- No passive evaluation
- No silent prompt transformation
- No hidden billing events

All protocol capabilities must be explicitly invoked by the model or client.

If a tool is not called, it does not execute.
If it does not execute, it does not bill.
If it does not bill, it does not record.

This is a hard mechanical boundary.

## Security Model

- API keys are never stored in plaintext  
- Only SHA-256 hashes are persisted  
- Billing uses a server-side service role  
- MCP tools expose no secret material  
- Ledger is append-only by design  

Tampering with billing, hashing, or ledger logic **voids the license**.

---

## License Model

This repository is **source-available**.

Commercial usage of the MCP server requires:

- a valid API key  
- sufficient credits  
- adherence to billing and ledger enforcement  

See `LICENSE` for full terms.

---

## Intended Users

This system is designed for:

- infrastructure engineers  
- AI platform builders  
- research systems  
- enterprise compute governance  
- operators working near thermodynamic or economic limits  

It is not designed for casual experimentation.

---

## Philosophy (Non-Marketing)

Chambers Protocol treats:

- Language as energy  
- Noise as heat  
- Billing as conservation  
- Determinism as cooling  

These are **not metaphors inside the system**.  
They are enforced mechanically.

---

## Status

**Production-ready**  
**Audited**  
**Live**
