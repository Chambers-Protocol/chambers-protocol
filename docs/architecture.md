# Architecture

This document describes the architecture of the Chambers Protocol MCP Server.

The system is designed to enforce **deterministic reasoning**, **atomic billing**, and **auditable execution** under concurrent load.

---

## Architectural Goals

The architecture exists to satisfy the following constraints:

1. **Determinism**  
   Identical inputs under identical state produce identical outcomes.

2. **Atomicity**  
   Credit consumption and execution authorization cannot be separated.

3. **Auditability**  
   Every successful execution is permanently recorded.

4. **Fail-Closed Behavior**  
   Any billing or authorization failure prevents execution.

5. **Separation of Concerns**  
   Control, billing, execution, and audit are isolated but coordinated.

---

## High-Level Components

The system consists of five primary components:

1. **Client / Host Environment**
2. **MCP Server (Chambers Node)**
3. **Billing & Ledger Backend (Postgres via Supabase)**
4. **Protocol Kernel**
5. **Audit Surface**

Each component has a strictly defined role.

---

## Component Overview

### 1. Client / Host Environment

Examples:
- Claude Desktop
- IDEs supporting MCP
- Automated agents

Responsibilities:
- Initiate MCP tool calls
- Supply natural-language input
- Never handle billing logic
- Never store ledger state

The client is untrusted with respect to billing.

---

### 2. MCP Server (Chambers Protocol Node)

The MCP server is the **control plane**.

Responsibilities:
- Expose MCP tools (`protocol.compile`, `meta.descriptor`, etc.)
- Enforce billing before execution
- Coordinate between billing backend and protocol kernel
- Reject unauthorized or unpaid requests

The MCP server never executes protocol logic until billing succeeds.

---

### 3. Billing & Ledger Backend (Postgres)

Implemented via:
- Supabase-hosted Postgres
- Server-side service role
- Postgres RPC (`consume_credits`)

Responsibilities:
- Store API key hashes
- Track remaining credits
- Enforce atomic credit decrement
- Insert immutable ledger entries

This backend is the **authoritative state machine** for execution permission.

---

### 4. Protocol Kernel

The kernel performs the deterministic transformation.

Responsibilities:
- Convert natural language into Chambers Syntax
- Enforce multiplicative grammar constraints
- Avoid narrative or anthropomorphic interpretation
- Return a deterministic instruction block to the model

The kernel is invoked **only after** billing authorization.

---

### 5. Audit Surface

The audit surface consists of:
- The `fidelity_ledger` table
- Read-only inspection endpoints
- Reconciliation queries

Responsibilities:
- Record all billed executions
- Support human and machine verification
- Enable dispute resolution

Audit mechanisms never influence execution flow.

---

## Execution Flow (Step-by-Step)

Client
|
| 1. MCP tool call (raw prompt)
v
MCP Server
|
| 2. Hash API key (SHA-256)
| 3. Call consume_credits RPC
v
Postgres (Atomic Transaction)
|
| 4a. Validate key & credit balance
| 4b. Decrement credits
| 4c. Insert ledger entry
v
MCP Server
|
| 5. Invoke Protocol Kernel
v
Kernel
|
| 6. Emit deterministic syntax
v
Client / Host Model


If any step prior to kernel invocation fails, execution halts.

---

## Atomic Billing Boundary

The atomic boundary is enforced inside Postgres.

Properties:
- Single transaction
- No read-then-write
- Serializable semantics
- Concurrency-safe

This ensures:
- Credits cannot be double-spent
- Ledger entries correspond to real executions
- System behavior is predictable under load

---

## Failure Domains

The system defines explicit failure domains:

| Domain | Result |
|---|---|
| Invalid API key | Execution denied |
| Insufficient credits | Execution denied |
| Billing backend offline | Execution denied |
| Kernel failure | Credits already consumed |
| Ledger write failure | Execution may proceed (audit degradation) |

Failures never result in unpaid execution.

---

## Trust Boundaries

| Boundary | Trust Level |
|---|---|
| Client | Untrusted |
| MCP Server | Trusted |
| Billing Backend | Trusted |
| Protocol Kernel | Trusted |
| Audit Ledger | Trusted |

Clients are never trusted to self-report usage.

---

## Scalability Characteristics

- MCP servers are stateless
- Billing backend is the single shared authority
- Horizontal scaling is supported
- Concurrency safety is guaranteed by the database

Scaling MCP nodes does not introduce billing inconsistencies.

---

## Security Considerations

- API keys are never stored in plaintext
- Only SHA-256 hashes are persisted
- Service role keys never leave the server
- Ledger is append-only
- Execution requires prior authorization

See `SECURITY.md` for vulnerability reporting and key handling.

---

## Design Non-Goals

The architecture intentionally does **not** attempt to:

- Optimize for conversational UX
- Hide billing mechanics
- Perform heuristic retries
- Abstract away failure states

Clarity is favored over convenience.

---

## Summary

The Chambers Protocol architecture enforces:

- Deterministic execution
- Atomic billing
- Immutable auditability
- Explicit failure modes

These properties are structural, not behavioral.

The system is designed to operate correctly under adversarial input, concurrency, and economic pressure.
