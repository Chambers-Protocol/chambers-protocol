## Stripe Checkout Link

➡️ https://buy.stripe.com/6oUeVf0Nv61GgWR5i81kA00

Purchasing Access to Chambers Protocol

This document describes the only supported method for purchasing access to the Chambers Protocol MCP Server.

Access is credit-based and enforced mechanically.

Product Definition

You are purchasing compute access credits, not software.

Item	Value
Product	Chambers Protocol Compute Credits
Cost per protocol invocation	10 credits
Fidelity tax per invocation  $0.04
Credit expiration	None

Credits are consumed atomically at execution time.

Purchase Flow (End-to-End)
Step 1 — Stripe Checkout

All purchases are processed via Stripe.

You will be directed to a Stripe checkout session configured for:

one-time payment

USD currency

fixed quantity (25,000 credits)

No subscription is required.

Step 2 — Payment Confirmation

After successful payment:

Stripe confirms the transaction server-side

No client-side confirmation is relied upon

Failed or incomplete payments result in no access being issued.

Step 3 — API Key Generation

Upon confirmed payment:

A cryptographically random API key is generated

The plaintext key is never stored

A SHA-256 hash of the key is stored in the ledger

The credit balance is initialized to 25,000 credits

The key is marked active

This process is non-interactive and deterministic.

Step 4 — Email Delivery

You will receive an email containing:

your API key (displayed once)

usage instructions

a reminder to store the key securely

If you lose the key, it cannot be recovered.

A new key must be issued and the old key revoked.

Using Your API Key

Your API key is required for all MCP server calls.

Internally:

the key is hashed with SHA-256

credits are deducted via atomic Postgres RPC

execution proceeds only on success

If credits are insufficient, the request is rejected.

Credit Consumption Rules

Credits are deducted before execution

Deduction is atomic

Failed deductions result in no execution

No partial execution is possible

There is no retry credit refund mechanism.

Fidelity Tax

Each protocol invocation generates a $0.04 USD fidelity tax.

This tax:

represents the cost of entropy reduction

is recorded in the fidelity ledger

is not refundable

is independent of execution success after billing

Audit & Transparency

All usage is recorded in a write-once ledger with:

timestamp

hashed API key

operation type

credit cost

fidelity tax amount

request identifier

This ledger is the authoritative source of truth.

Refund Policy

Credits are non-refundable once issued.

Stripe disputes do not retroactively invalidate:

issued API keys

consumed credits

ledger entries

Abuse or chargebacks may result in key revocation.

Security Responsibilities (Customer)

You are responsible for:

safeguarding your API key

preventing unauthorized usage

rotating compromised keys immediately

The system does not distinguish between users of the same key.

Support

For purchase-related issues:

use the GitHub issue template “Purchase Support”

include your Stripe receipt ID

do not include your API key in plaintext

Summary

Payment → Stripe

Fulfillment → deterministic

Access → credit-gated

Billing → atomic

Auditing → append-only

Guarantees → mechanical

If you want to proceed, initiate checkout via Stripe.