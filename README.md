# FinBrain MCP&nbsp;<!-- omit in toc -->

[![PyPI version](https://img.shields.io/pypi/v/finbrain-mcp.svg)](https://pypi.org/project/finbrain-mcp/)
[![CI](https://github.com/ahmetsbilgin/finbrain-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/ahmetsbilgin/finbrain-mcp/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)

> **Requires Python 3.10+**

A **Model Context Protocol (MCP)** server that exposes FinBrain datasets to AI clients (Claude Desktop, VS Code MCP extensions, etc.) via simple tools.  
Backed by the official **`finbrain-python`** SDK.

- Package name: **`finbrain-mcp`**

- CLI entrypoint: **`finbrain-mcp`**

----------

## What you get

- ⚡️ **Local** MCP server (no proxying) using your **own FinBrain API key**

- 🧰 Tools (JSON by default, CSV optional) with paging

  - `health`

  - `available_markets`, `available_tickers`

  - `predictions_by_market`, `predictions_by_ticker`

  - `news_sentiment_by_ticker`

  - `app_ratings_by_ticker`

  - `analyst_ratings_by_ticker`

  - `house_trades_by_ticker`

  - `insider_transactions_by_ticker`

  - `linkedin_metrics_by_ticker`

  - `options_put_call`

- 🧹 Consistent, model-friendly shapes (we normalize raw API responses)

- 🔑 Multiple ways to provide your API key: env var, file

----------

## Install

### Option A — Standard install (pip)

```bash
# macOS / Linux / Windows
pip install --upgrade finbrain-mcp
```

### Option B — Dev install (editable)

```bash
# from repo root
python -m venv .venv
source .venv/bin/activate # Windows: .\.venv\Scripts\activate
pip install -e ".[dev]"
```

> Keep **pip** (prod) and your **venv** (dev) separate to avoid path mix-ups.

----------

## Configure your FinBrain API key

### A) In your MCP client config (recommended / most reliable)

Put the key directly in the MCP server entry your client uses (Claude Desktop or a VS Code MCP extension). This guarantees the launched server sees it, even if system env vars aren’t picked up.

#### Claude Desktop (pip install)

```json
{
  "mcpServers": {
    "finbrain": {
      "command": "finbrain-mcp",
      "env": { "FINBRAIN_API_KEY": "YOUR_KEY" }
    }
  }
}
```

### B) Environment variable

This works too, but note you must restart the client after setting it so the new value is inherited.

```bash
# macOS/Linux
export FINBRAIN_API_KEY="YOUR_KEY"

# Windows (PowerShell, current session)
$env:FINBRAIN_API_KEY="YOUR_KEY"

# Windows (persistent for new processes)
setx FINBRAIN_API_KEY "YOUR_KEY"
# then fully quit and reopen your MCP client (e.g., Claude Desktop)
```

>**Tip:** If the env var route doesn’t seem to work (common on Windows if the client was already running), use the **config JSON `env`** method above—it’s more deterministic.
----------

## Run the server

> **Note:** You typically don’t need to run the server manually—your MCP client (Claude/VS Code) starts it automatically. Use the commands below only for manual checks or debugging.

- If installed (pip):

    `finbrain-mcp`

- From a dev venv:

    `python -m finbrain_mcp.server`

Quick health check without an MCP client:

```python
python - <<'PY'
import json
from finbrain_mcp.tools.health import health
print(json.dumps(health(), indent=2))
PY
```

----------

## Connect an AI client

> **No manual start needed:** Claude Desktop and VS Code will **launch the MCP server for you** based on your config. You only need to run `finbrain-mcp` yourself for quick sanity checks or debugging.

### Claude Desktop

Edit your config:

- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

- Linux: `~/.config/Claude/claude_desktop_config.json`

**Pip install (published package):**

```json
{
  "mcpServers": {
    "finbrain": {
      "command": "finbrain-mcp",
      "env": { "FINBRAIN_API_KEY": "YOUR_KEY" }
    }
  }
}

```

**macOS tip (full path):** If `"command": "finbrain-mcp"` doesn’t work, find the absolute path and use that instead.

```bash
which finbrain-mcp    # macOS/Linux
# (Windows: where finbrain-mcp)
```

**Claude config with full path (macOS example):**

```json
{
  "mcpServers": {
    "finbrain": {
      "command": "/usr/local/bin/finbrain-mcp",
      "env": { "FINBRAIN_API_KEY": "YOUR_KEY" }
    }
  }
}
```

**Dev venv (run the module explicitly):**

```json
{
  "mcpServers": {
    "finbrain-dev": {
      "command": "C:\\Users\\you\\path\\to\\repo\\.venv\\Scripts\\python.exe",
      "args": ["-m", "finbrain_mcp.server"],
      "env": { "FINBRAIN_API_KEY": "YOUR_KEY" }
    }
  }
}
```

> After editing, **quit & reopen Claude**.

### VS Code (MCP)

1. Open the Command Palette → **“MCP: Open User Configuration”**.  
   This opens your `mcp.json` (user profile).
2. Add the server under the **`servers`** key:

    ```json
    {
      "servers": {
        "finbrain": {
          "command": "finbrain-mcp",
          "env": { "FINBRAIN_API_KEY": "YOUR_KEY" }
        }
      }
    }
    ```

3. In Copilot Chat, enable Agent Mode to use MCP tools.

----------

## What can you ask the agent?

You don’t need to know tool names—just ask in plain English. Examples:

- **Predictions**
  - “Get FinBrain’s **daily predictions** for **AMZN**.”
  - “Show **monthly predictions** (12-month horizon) for **AMZN**.”

- **News sentiment**
  - “What’s the **news sentiment** for **AMZN** **from 2025-01-01 to 2025-03-31** (limit 50)?”
  - “Export **AMZN** news sentiment for **2025 YTD** **as CSV**.”

- **App ratings**
  - “Fetch **app store ratings** for **AMZN** between **2025-01-01** and **2025-06-30**.”

- **Analyst ratings**
  - “List **analyst ratings** for **AMZN** in **Q1 2025**.”

- **House trades**
  - “Show **recent House trades** involving **AMZN**.”

- **Insider transactions**
  - “Recent **insider transactions** for **AMZN**?”

- **LinkedIn metrics**
  - “Get **LinkedIn employee & follower counts** for **AMZN** (last 12 months).”

- **Options (put/call)**
  - “What’s the **put/call ratio** for **AMZN** over the **last 60 days**?”

- **Availability**
  - “Which **markets** are available?”
  - “List **tickers** in the **daily** predictions universe.”

> **Notes**
>
> - Date format: `YYYY-MM-DD`.
> - Time-series endpoints return the **most recent N** points by default—say “limit 200” to get more.
> - Predictions horizon: **daily** (10-day) or **monthly** (12-month).
> - Say “**as CSV**” to receive CSV instead of JSON.

----------

## Development

```bash
# setup
python -m venv .venv
source .venv/bin/activate # Windows: .\.venv\Scripts\activate
pip install -e ".[dev]"  # run tests pytest -q
```

### Project structure (high level)

```text
finbrain-mcp
├─ README.md
├─ pyproject.toml
├─ LICENSE
├─ .github/
├─ examples/
├─ src/
│  └─ finbrain_mcp/
│     ├─ __init__.py
│     ├─ server.py                # MCP server entrypoint
│     ├─ registry.py              # FastMCP instance
│     ├─ client_adapter.py        # wraps finbrain-python; calls normalizers
│     ├─ auth.py                  # resolves API key (env var)
│     ├─ settings.py              # tweakable defaults (e.g., series limits)
│     ├─ utils.py                 # helpers (latest_slice, CSV, DF->records)
│     ├─ normalizers/             # endpoint-specific shapers
│     └─ tools/                   # MCP tool functions (registered & testable)
└─ tests/                         # pytest suite with a fake SDK
```

----------

## Troubleshooting

- **`ENOENT`** (can’t start server)

  - Wrong path in client config. Use the venv’s **exact** path:

    - `…\.venv\Scripts\python.exe` + `["-m","finbrain_mcp.server"]`, or

    - `…\.venv\Scripts\finbrain-mcp.exe`

- **`FinBrain API key not configured`**

  - Put `FINBRAIN_API_KEY` in the client’s `env` block **or**

  - `setx FINBRAIN_API_KEY "YOUR_KEY"` and fully restart the client.

- **Mixing dev & prod installs**

  - Keep **pip** (prod) and **venv** (dev) separate.

  - In configs, point to one or the other—not both.

----------

## License

MIT (see `LICENSE`).

----------

## Acknowledgements

- Built on Model Context Protocol and **FastMCP**.

- Uses the official **`finbrain-python`** SDK.

----------

© 2025 FinBrain Technologies — Built with ❤️ for the quant community.
