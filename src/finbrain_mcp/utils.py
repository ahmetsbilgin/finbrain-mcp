from __future__ import annotations
from typing import Any, Iterable, Dict


def latest_slice(rows: list[dict] | list[Any], limit: int) -> list:
    """
    Return the last `limit` items, preserving original order.

    Assumes `rows` is in ascending chronological order, so the last `limit`
    items are the most recent ones. Normalizers sort series ascending by date
    before this is applied; pass already-ascending data to get "most recent N".
    """
    rows = list(rows or [])
    if limit <= 0:
        return []
    if limit >= len(rows):
        return rows
    return rows[-limit:]


def limit_slice(rows: list[dict] | list[Any], offset: int, limit: int) -> list:
    if offset < 0:
        offset = 0
    if limit <= 0:
        return []
    return rows[offset : offset + limit]


def rows_to_csv(rows: Iterable[Dict]) -> str:
    import io
    import csv

    rows = list(rows)
    if not rows:
        return ""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()


def df_to_records_maybe(obj: Any) -> Any:
    """
    If obj is a pandas DataFrame/Series, convert to JSON records; if it is
    already a list, return it unchanged. Any other shape is returned as-is so
    callers (which guard with isinstance checks) can decide how to handle it.
    """
    try:
        import pandas as pd  # type: ignore[import-untyped]

        if isinstance(obj, pd.DataFrame):
            df = obj.copy()
            for c in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[c]):
                    df[c] = df[c].dt.strftime("%Y-%m-%d")
            return df.to_dict(orient="records")
        if isinstance(obj, pd.Series):
            return [obj.to_dict()]
    except Exception:
        pass
    return obj
