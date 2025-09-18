from __future__ import annotations
from .registry import mcp
from .auth import resolve_api_key
from .client_adapter import FBClient

# Import tool modules so their @tool functions register
from .tools import availability  # noqa: F401
from .tools import app_ratings  # noqa: F401
from .tools import analyst_ratings  # noqa: F401
from .tools import house_trades  # noqa: F401
from .tools import insider_transactions  # noqa: F401
from .tools import linkedin  # noqa: F401
from .tools import options  # noqa: F401
from .tools import predictions  # noqa: F401
from .tools import sentiments  # noqa: F401
from .tools import health  # noqa: F401


# Eagerly resolve to fail fast with a good error if misconfigured
def _make_client() -> FBClient:
    key = resolve_api_key()
    return FBClient(key)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
