from __future__ import annotations
from typing import Any


def to_int(x):
    if x is None:
        return None
    try:
        return int(x)
    except (TypeError, ValueError):
        try:
            return int(float(x))
        except Exception:
            return None


def to_float(x: Any) -> float | None:
    if x is None:
        return None
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def pct_to_ratio(x):
    if x is None:
        return None
    try:
        return float(x) / 100.0
    except Exception:
        return None


def pct_to_text(x, decimals: int = 2):
    if x is None:
        return None
    try:
        return f"{float(x):.{decimals}f}%"
    except Exception:
        return None


def parse_mid_low_high(triplet: Any) -> dict:
    """
    RAW string like '201.33,197.21,205.45' -> {'mid': 201.33, 'low': 197.21, 'high': 205.45}
    """
    s = str(triplet) if triplet is not None else ""
    parts = [p.strip() for p in s.split(",")]
    mid = to_float(parts[0]) if len(parts) > 0 else None
    low = to_float(parts[1]) if len(parts) > 1 else None
    high = to_float(parts[2]) if len(parts) > 2 else None
    return {"mid": mid, "low": low, "high": high}
