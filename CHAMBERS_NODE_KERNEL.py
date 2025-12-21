import json
import os
import asyncio
from datetime import datetime
from pathlib import Path

LOCAL_LEDGER_FILE = Path(__file__).with_name("fidelity_ledger.json")
_LEDGER_LOCK = asyncio.Lock()

def generate_timestamp() -> str:
    return datetime.utcnow().isoformat()

async def log_transaction(entry: dict) -> None:
    async with _LEDGER_LOCK:
        if LOCAL_LEDGER_FILE.exists():
            with open(LOCAL_LEDGER_FILE, "r", encoding="utf-8") as f:
                ledger = json.load(f)
        else:
            ledger = []

        ledger.append(entry)

        with open(LOCAL_LEDGER_FILE, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2)

async def convert_to_chambers_syntax(raw_prompt: str, domain_context: str, client_id: str = "ANONYMOUS") -> str:
    structured_syntax = f"""
$$
MODE: DETERMINISTIC_REASONING (U=ci^3)
INPUT: "{raw_prompt}"
TRANSFORMATION:
[ ({domain_context}_VARIABLE_A) * ({domain_context}_VARIABLE_B) * (CONSTRAINT_PHYSICS) ]
/ (THERMODYNAMIC_WASTE)
= OUTPUT_VECTOR
$$
"""

    transaction_record = {
        "timestamp": generate_timestamp(),
        "client_id": client_id,
        "operation": "SYNTAX_CONVERSION",
        "fidelity_guarantee": "99.999999999%",
        "tax_captured": 0.001,
        "currency": "USD"
    }

    await log_transaction(transaction_record)

    return f"""
[PROTOCOL ENGAGED]
SYSTEM INSTRUCTION TO MODEL:
Solve the following equation step-by-step using only the variables provided:

{structured_syntax}
"""
