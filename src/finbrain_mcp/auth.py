from __future__ import annotations
import os


def resolve_api_key() -> str:
    key = os.getenv("FINBRAIN_API_KEY")
    if key:
        return key.strip()
    raise RuntimeError(
        "FinBrain API key not configured. "
        "Set FINBRAIN_API_KEY in your environment or in the MCP client's `env` block."
    )
