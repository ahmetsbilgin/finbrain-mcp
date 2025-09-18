from __future__ import annotations
from importlib.metadata import version as pkg_version
from ..registry import mcp
from ..auth import resolve_api_key
from ..client_adapter import FBClient
from .. import __version__


def health() -> dict:
    """
    Basic server health & version info. Tries to resolve the API key and
    construct the SDK client (no network call), then returns versions.
    """
    try:
        key = resolve_api_key()
        _ = FBClient(key)  # init only; verifies config path is OK
        ok = True
        err = None
    except Exception as e:
        ok = False
        err = str(e)

    try:
        sdk_ver = pkg_version("finbrain-python")
    except Exception:
        sdk_ver = None

    return {
        "ok": ok,
        "error": err,
        "mcp_version": __version__,
        "sdk": {"package": "finbrain-python", "version": sdk_ver},
    }


mcp.tool()(health)
