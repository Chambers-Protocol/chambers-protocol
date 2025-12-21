# Audit & Ledger Verification

This document describes how usage, billing, and fidelity guarantees are audited within the Chambers Protocol.

The audit surface is **mechanical**, **deterministic**, and **append-only**.

---

## Authoritative Sources of Truth

There are two authoritative data planes:

1. **Credits Balance**
   - Stored in the `api_keys` table
   - Updated atomically via Postgres RPC
   - Represents remaining execution capacity

2. **Fidelity Ledger**
   - Stored in the `fidelity_ledger` table
   - Append-only
   - Records every protocol invocation that successfully consumed credits

No other system state is considered authoritative.

---

## Ledger Design Principles

The fidelity ledger is designed with the following constraints:

- **Append-only**: no updates or deletes permitted
- **Deterministic writes**: entries are generated programmatically
- **Human-auditable**: readable SQL queries
- **Machine-verifiable**: consistent schema and invariants
- **Non-blocking**: audit writes never gate execution success

The ledger is not used for control flow.
It is used for **verification and reconciliation**.

---

## Ledger Schema (Canonical Fields)

Each row in `fidelity_ledger` contains:

| Field | Description |
|---|---|
| `id` | Monotonic identity (primary key) |
| `created_at` | Timestamp of invocation |
| `client_email` | Email associated with API key |
| `api_key_hash` | SHA-256 hash of API key |
| `operation` | Operation type (e.g. `PROTOCOL_COMPILE`) |
| `credits_cost` | Credits consumed by this invocation |
| `fidelity_tax_usd` | USD-denominated fidelity tax |
| `request_id` | UUID for correlation |
| `metadata` | JSON payload with contextual data |

All monetary values are recorded explicitly.

---

## Atomicity Guarantees

Credit consumption and ledger insertion are performed inside a **single Postgres transaction** via the `consume_credits` RPC function.

This guarantees:

- Credits are deducted **only if** the ledger entry is written
- Ledger entries exist **only if** credits were successfully deducted
- No race conditions between read and write operations

If the RPC fails, **no state change occurs**.

---

## Audit Invariants

The following invariants must always hold:

1. Credits never increase except via explicit purchase allocation
2. Credits never decrease without a corresponding ledger entry
3. Ledger entries are never modified after insertion
4. Each ledger entry represents a successful, billed invocation
5. Request IDs are globally unique

Violation of any invariant indicates a system fault.

---

## Common Audit Queries

1. Inspect recent ledger entries

```sql
select
  created_at,
  client_email,
  operation,
  credits_cost,
  fidelity_tax_usd,
  request_id
from public.fidelity_ledger
order by created_at desc
limit 20;

2. Verify remaining credits for a client
select
  client_email,
  credits_remaining
from public.api_keys
where client_email = 'user@example.com';

3. Reconcile total credits consumed vs ledger
select
  sum(credits_cost) as total_credits_billed
from public.fidelity_ledger
where client_email = 'user@example.com';

Compare against initial allocation:

initial_credits - total_credits_billed = credits_remaining

4. Verify fidelity tax accrual
select
  sum(fidelity_tax_usd) as total_fidelity_tax
from public.fidelity_ledger
where client_email = 'user@example.com';

5. Detect anomalies (should return zero rows)
select *
from public.api_keys ak
where ak.credits_remaining < 0;