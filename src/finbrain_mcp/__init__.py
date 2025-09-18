# FinBrain MCP package
try:
    # written by setuptools-scm at build time
    from ._version import __version__  # type: ignore
except Exception:  # pragma: no cover
    try:
        from importlib.metadata import version

        __version__ = version("finbrain-mcp")
    except Exception:
        __version__ = "0.0.0"
