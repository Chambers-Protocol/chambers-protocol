# Chambers Protocol  
**Deterministic Reasoning Infrastructure for Entropy-Bound Systems**

[![Checkout $1,000 for 1,000,000 Credits](https://img.shields.io/badge/Checkout-$1,000%20for%201,000,000%20credits-black)](https://buy.stripe.com/6oUeVf0Nv61GgWR5i81kA00)
![Billing](https://img.shields.io/badge/Billing-Atomic-green)
![Ledger](https://img.shields.io/badge/Ledger-Append--Only-blue)
![Pricing](https://img.shields.io/badge/Price-$0.01%20per%20call-black)

---

## Purchase Access

**$1,000 USD → 1,000,000 Credits**  
Each invocation consumes **10 credits** and generates a **$0.01 USD fidelity tax**.

➡️ **Stripe Checkout:**  
https://buy.stripe.com/6oUeVf0Nv61GgWR5i81kA00

> After payment, your API key is generated and delivered via email.

Alternative workflow:  
Open a purchase request on GitHub:  
https://github.com/Chambers-Protocol/chambers-protocol/issues/new?template=purchase.yml

---

## Overview

Chambers Protocol is a mechanically enforced reasoning and billing layer operating at the boundary between **human input** and **machine computation**.

It exists to address a hard constraint:

- Unbounded language generates entropy  
- Entropy generates heat  
- Heat limits computation  

Chambers Protocol constrains this process by enforcing **deterministic transformation**, **atomic accounting**, and **auditable cost surfaces** at the moment computation is invoked.

This repository hosts the **production MCP Server implementation**.

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

## Pricing

| Item | Value |
|----|----|
| Initial purchase | $1,000 USD |
| Credits received | 1,000,000 |
| Cost per MCP call | 10 credits |
| Fidelity tax per call | $0.01 USD |
| Credit expiration | Never |

Credits are consumed **atomically at invocation time** via Postgres RPC.  
If credits cannot be deducted, execution **does not occur**.

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
