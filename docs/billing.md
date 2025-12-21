# Billing & Credit Accounting

This document defines how billing, credit consumption, and fidelity taxation operate within the Chambers Protocol.

Billing is **mechanical**, **deterministic**, and enforced **prior to execution**.

---

## Billing Model Overview

Chambers Protocol operates on a **prepaid credit model**.

- Credits represent execution capacity
- Credits are consumed atomically
- Billing occurs **before** protocol execution
- No execution occurs without successful billing

There is no post-hoc billing or reconciliation required for normal operation.

---

## Credit Units

| Attribute | Value |
|---|---|
| Initial allocation | 1,000,000 credits |
| Cost per invocation | 10 credits |
| Credit expiration | None |
| Minimum balance | 0 |

Credits are integers and are decremented deterministically.

---

## Fidelity Tax

Each successful protocol invocation generates a **fidelity tax**.

| Attribute | Value |
|---|---|
| Fidelity tax per invocation | $0.01 USD |
| Currency | USD |
| Precision | Fixed (numeric, two decimal places) |

The fidelity tax represents the cost of entropy reduction and protocol enforcement.

The tax is recorded in the fidelity ledger for audit purposes.

---

## Execution Order (Strict)

The protocol enforces the following order:

1. API key hash is computed (SHA-256)
2. Credit availability is checked
3. Credits are decremented atomically
4. Fidelity ledger entry is written
5. Protocol execution is permitted

If any step prior to execution fails, **execution does not occur**.

---

## Atomic Billing Enforcement

Billing is enforced via a **Postgres RPC function** (`consume_credits`).

Properties:

- Single transaction
- No read-then-write logic
- No race conditions
- Serializable at the database level

This guarantees that:

- Credits cannot be double-spent
- Ledger entries correspond to real executions
- System state cannot drift under concurrency

---

## Billing Failure Modes

### 1. Insufficient Credits

- RPC returns an error
- Credits are not decremented
- No ledger entry is written
- Execution is denied

### 2. Invalid API Key

- RPC returns an error
- No state is modified
- Execution is denied

### 3. Billing System Offline

- Execution is denied
- No credits are consumed
- No ledger entry is written

This system fails **closed**, not open.

---

## Ledger Relationship

Billing and audit are related but not identical concerns:

- **Credits** control execution
- **Ledger entries** provide verification and reconciliation

Credits determine *whether* execution happens.  
The ledger records *that* it happened.

See `docs/audit.md` for verification procedures.

---

## Credit Allocation

Credits are allocated only via:

- Stripe-confirmed purchase
- Explicit administrative issuance

Credits are never minted dynamically during execution.

---

## Refunds & Chargebacks

- Credits are non-refundable once issued
- Consumed credits cannot be reversed
- Chargebacks may result in API key revocation

Ledger entries remain immutable regardless of payment disputes.

---

## Usage Transparency

Licensees are able to:

- Inspect remaining credits
- Reconcile credits against ledger entries
- Verify fidelity tax accumulation

The system is designed so that no trust in the operator is required.

---

## Design Rationale

The billing model exists to enforce three constraints:

1. **Conservation**  
   Execution consumes a finite resource.

2. **Determinism**  
   Billing outcomes are predictable and repeatable.

3. **Auditability**  
   All usage can be independently verified.

Billing is not an add-on.
It is a core protocol primitive.

---

## Summary

- Billing is prepaid and credit-based
- Credits are consumed atomically
- Fidelity tax is fixed and auditable
- Execution is gated by successful billing
- The system fails closed under error conditions

The Chambers Protocol treats billing as a first-class systems concern.
