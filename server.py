# server.py — mechanically hardened (final form)
# - Deterministic hashing (sha256, NO python hash())
# - Atomic decrement via Postgres RPC (consume_credits) instead of read-then-write
# - Tool names aligned to descriptor: meta.descriptor, protocol.compile, ledger.evaluate
# - Secrets loaded from .env, never printed; logs go to stderr
# - Descriptor served from mcp.descriptor.json
# - Local ledger inspection is read-only and tolerant of missing/empty/corrupt JSON
# - Supabase audit insert is best-effort (non-blocking)
# - Type hints compatible with Python 3.10+ (no PEP604 union operator needed)

import os
import sys
import json
import hashlib
from pathlib import Path
from typing import Any, Dict, Optional, Union

from dotenv import load_dotenv
from supabase import create_client, Client
from mcp.server.fastmcp import FastMCP

import CHAMBERS_NODE_KERNEL as kernel

# ----------------------------
# 1) CONFIGURATION & SECRETS
# ----------------------------
BASE_DIR = Path(__file__).parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

# Supabase:
#   SUPABASE_URL: https://<project>.supabase.co
#   SUPABASE_SERVICE_ROLE_KEY: service role key (server-side only)
SUPABASE_URL = os.getenv("SUPABASE_URL") or os.getenv("CENTRAL_LEDGER_URL") or ""
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("CENTRAL_LEDGER_SECRET") or ""

# Single-user node mode: plaintext key stored in env; hashed deterministically per request.
NODE_API_KEY = os.getenv("CHAMBERS_API_KEY", "")

DESCRIPTOR_PATH = BASE_DIR / "mcp.descriptor.json"
LOCAL_LEDGER_FILE = BASE_DIR / "fidelity_ledger.json"

# Initialize MCP Server
mcp = FastMCP("Chambers Protocol Node")

# ----------------------------
# 2) DATABASE CONNECTION
# ----------------------------
supabase: Optional[Client] = None

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    print("❌ CRITICAL: Supabase URL/service key missing. Billing is disabled.", file=sys.stderr)
else:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
        print("✅ CONNECTED: Supabase link established.", file=sys.stderr)
    except Exception as e:
        print(f"❌ CONNECTION FAILED: {e}", file=sys.stderr)
        supabase = None

# ----------------------------
# 3) DESCRIPTOR LOADER
# ----------------------------
def load_descriptor() -> Dict[str, Any]:
    if not DESCRIPTOR_PATH.exists():
        # Deterministic failure payload (still a dict)
        return {
            "schema": "mcp.descriptor.v1",
            "error": "DESCRIPTOR_NOT_FOUND",
            "path": str(DESCRIPTOR_PATH),
        }
    try:
        return json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        return {
            "schema": "mcp.descriptor.v1",
            "error": "DESCRIPTOR_INVALID_JSON",
            "detail": str(e),
            "path": str(DESCRIPTOR_PATH),
        }

# ----------------------------
# 4) CRYPTO HASHING (DETERMINISTIC)
# ----------------------------
def key_hash(api_key: str) -> str:
    """
    Deterministic hash for DB lookup; store this hex digest in api_keys.api_key_hash.
    """
    # NOTE: do NOT .strip() — whitespace changes would desync stored hashes.
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()

# ----------------------------
# 5) BILLING ENGINE (ATOMIC)
# ----------------------------
def _extract_supabase_error(resp: Any) -> Optional[str]:
    """
    supabase-py response compatibility shim across versions.
    """
    err = getattr(resp, "error", None)
    if err:
        return str(err)
    # Some versions surface errors differently; keep it safe.
    return None

def consume_credits_atomic(api_key: str, cost: int) -> Dict[str, Any]:
    """
    Strict mode:
      - Calls Postgres RPC consume_credits(p_api_key_hash, p_cost)
      - Raises on invalid key / insufficient credits / connection issues

    Returns: a single row dict: {"client_email": ..., "credits_remaining": ...}
    """
    if not supabase:
        raise RuntimeError("BILLING_OFFLINE")

    if not api_key:
        raise RuntimeError("MISSING_API_KEY")

    if cost <= 0:
        raise ValueError("INVALID_COST")

    api_key_h = key_hash(api_key)

    # RPC: public.consume_credits(text,int)
    resp = supabase.rpc("consume_credits", {"p_api_key_hash": api_key_h, "p_cost": int(cost)}).execute()

    err = _extract_supabase_error(resp)
    if err:
        raise RuntimeError(f"RPC_ERROR: {err}")

    data = getattr(resp, "data", None)
    if data is None or data == []:
        raise RuntimeError("INVALID_KEY_OR_INSUFFICIENT_CREDITS")

    # Normalize list-of-rows -> single row dict
    if isinstance(data, list):
        row = data[0] if data else {}
    elif isinstance(data, dict):
        row = data
    else:
        # Unexpected shape
        raise RuntimeError(f"RPC_UNEXPECTED_RESPONSE_TYPE: {type(data).__name__}")

    return row

# Optional: additional audit trail table (non-blocking)
def insert_audit_event(client_id: str, operation: str, tax_captured: int) -> None:
    if not supabase:
        return
    try:
        supabase.table("fidelity_ledger").insert({
            "client_id": client_id,
            "operation": operation,
            "tax_captured": tax_captured
        }).execute()
    except Exception:
        # Best-effort only; never break tool execution.
        pass

# ----------------------------
# 6) TOOLS
# ----------------------------
@mcp.tool(name="meta_descriptor")
def meta_descriptor() -> Dict[str, Any]:
    return load_descriptor()

@mcp.tool(name="protocol_compile")
async def protocol_compile(raw_prompt: str) -> str:
    cost = 10

    if not NODE_API_KEY:
        return "[[ACCESS DENIED]] Missing CHAMBERS_API_KEY on node."

    try:
        row = consume_credits_atomic(NODE_API_KEY, cost)

        client_email = row.get("client_email", "UNKNOWN")
        remaining = row.get("credits_remaining", None)

        print(f"[BILLING SUCCESS] client={client_email} remaining={remaining}", file=sys.stderr)
        insert_audit_event(client_email, "PROTOCOL_COMPILE", cost)

    except Exception as e:
        print(f"[BILLING FAILURE] {type(e).__name__}: {e}", file=sys.stderr)
        return "[[ACCESS DENIED]] Payment failed, invalid key, or insufficient credits."

    return await kernel.convert_to_chambers_syntax(
        raw_prompt=raw_prompt,
        domain_context="ENTERPRISE_PHYSICS",
        client_id="PRODUCTION_USER"
    )

@mcp.tool(name="ledger_evaluate")
def ledger_evaluate(client_id: str = "", limit: int = 50) -> Dict[str, Any]:
    ...


@mcp.tool(name="ledger_evaluate")
def ledger_evaluate(client_id: str = "", limit: int = 50) -> Dict[str, Any]:
    """
    Read-only local ledger inspection (fidelity_ledger.json).
    Deterministic. No billing.
    """
    if limit <= 0:
        return {"entries": [], "count": 0}

    if not LOCAL_LEDGER_FILE.exists():
        return {"entries": [], "count": 0}

    try:
        raw = LOCAL_LEDGER_FILE.read_text(encoding="utf-8").strip()
        if not raw:
            return {"entries": [], "count": 0}
        entries = json.loads(raw)
        if not isinstance(entries, list):
            return {"entries": [], "count": 0}
    except Exception:
        return {"entries": [], "count": 0}

    if client_id:
        entries = [
            e for e in entries
            if isinstance(e, dict) and (e.get("client_id") == client_id or e.get("client") == client_id)
        ]

    entries = entries[-limit:]
    return {"count": len(entries), "entries": entries}

# ----------------------------
# 7) RUN
# ----------------------------
if __name__ == "__main__":
    mcp.run()
