# FinBrain MCP&nbsp;<!-- omit in toc -->

[![PyPI version](https://img.shields.io/pypi/v/finbrain-mcp.svg)](https://pypi.org/project/finbrain-mcp/)
[![CI](https://github.com/ahmetsbilgin/finbrain-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/ahmetsbilgin/finbrain-mcp/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)

> **Requires Python 3.10+**

A **Model Context Protocol (MCP)** server that exposes FinBrain datasets to AI clients (Claude Desktop, VS Code MCP extensions, etc.) via simple tools.
Backed by the official **`finbrain-python`** SDK (v2 API).

- Package name: **`finbrain-mcp`**

- CLI entrypoint: **`finbrain-mcp`**

- Documentation: **[finbrain.tech/integrations/mcp](https://finbrain.tech/integrations/mcp/)**

----------

## Features

### AI-Powered Price Predictions

Access FinBrain's machine learning price forecasts with daily (10-day) and monthly (12-month) horizons. Includes mean predictions with 95% confidence intervals.

### News & Sentiment Analysis

Browse recent news articles for any ticker, or track aggregated daily sentiment scores over time. Screen news across all tracked stocks.

### Alternative Data

- **LinkedIn Metrics** — Employee count and follower trends as company health indicators
- **App Store Ratings** — Mobile app performance data for consumer-facing companies
- **Options Flow** — Put/call ratios and volume to gauge market positioning
- **Reddit Mentions** — Ticker mention counts across subreddits, collected every 4 hours
- **Government Contracts** — U.S. government contract awards from USAspending.gov

### Institutional & Insider Activity

- **US Congress Trades** — Stock transactions disclosed by House representatives and Senators
- **Corporate Lobbying** — Lobbying filings with registrant, income, expenses, and issue codes
- **Insider Transactions** — SEC Form 4 filings showing executive buys and sells
- **Analyst Ratings** — Wall Street coverage and price target changes

----------

## What you get

- ⚡️ **Local** MCP server (no proxying) using your **own FinBrain API key**

- 🧰 Tools (JSON by default, CSV optional) with paging

  - `health`

  - `available_markets`, `available_tickers`, `available_regions`

  - `predictions_by_market`, `predictions_by_ticker`

  - `news_by_ticker`, `news_sentiment_by_ticker`

  - `app_ratings_by_ticker`

  - `analyst_ratings_by_ticker`

  - `house_trades_by_ticker`, `senate_trades_by_ticker`

  - `corporate_lobbying_by_ticker`

  - `insider_transactions_by_ticker`

  - `linkedin_metrics_by_ticker`

  - `options_put_call`

  - `reddit_mentions_by_ticker`

  - `government_contracts_by_ticker`

  - `recent_news`, `recent_analyst_ratings`

  - `screener_sentiment`, `screener_analyst_ratings`, `screener_news`

  - `screener_insider_trading`, `screener_house_trades`, `screener_senate_trades`

  - `screener_put_call_ratio`, `screener_linkedin`, `screener_app_ratings`, `screener_reddit_mentions`, `screener_government_contracts`

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

### Option C — Docker

```bash
# Build the image
docker build -t finbrain-mcp:latest .

# Run with your API key
docker run --rm -e FINBRAIN_API_KEY="YOUR_KEY" finbrain-mcp:latest
```

> See [DOCKER.md](DOCKER.md) for detailed Docker usage instructions.

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

**macOS tip (full path):**

If `"command": "finbrain-mcp"` doesn’t work, find the absolute path and use that instead.

```bash
which finbrain-mcp    # macOS/Linux
# (Windows: where finbrain-mcp)
```

**Claude config with full path (macOS example):**

```json
{
  "mcpServers": {
    "finbrain": {
      "command": "/full/path/to/finbrain-mcp",
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

**Docker:**

```json
{
  "mcpServers": {
    "finbrain": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "finbrain-mcp:latest"],
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
  - “Get **market-wide daily predictions** for **S&P 500** tickers.”

- **News**
  - “Get **recent news articles** for **AMZN**.”
  - “What’s the **news sentiment** for **AMZN** **from 2025-01-01 to 2025-03-31** (limit 50)?”
  - “Show me the **latest news** across all **S&P 500** stocks.”

- **App ratings**
  - “Fetch **app store ratings** for **AMZN** between **2025-01-01** and **2025-06-30**.”

- **Analyst ratings**
  - “List **analyst ratings** for **AMZN** in **Q1 2025**.”

- **Congressional trades**
  - “Show **recent House trades** involving **AMZN**.”
  - “Show **recent Senate trades** involving **META**.”

- **Corporate lobbying**
  - “Show **corporate lobbying filings** for **AAPL**.”
  - “What **lobbying firms** has **MSFT** used in **2024** (from 2024-01-01 to 2024-12-31)?”

- **Insider transactions**
  - “Recent **insider transactions** for **AMZN**?”

- **LinkedIn metrics**
  - “Get **LinkedIn employee & follower counts** for **AMZN** (last 12 months).”

- **Options (put/call)**
  - “What’s the **put/call ratio** for **AMZN** over the **last 60 days**?”

- **Reddit mentions**
  - “Show **Reddit mentions** for **TSLA** over the **last week**.”
  - “Which **subreddits** are talking about **AAPL** the most?”

- **Government contracts**
  - “Show **government contracts** awarded to **LMT** in **2025**.”
  - “Which companies have the **largest government contract awards**?”

- **Screeners (cross-ticker)**
  - “Screen **sentiment** across **S&P 500** stocks.”
  - “Show the **latest analyst ratings** across all stocks.”
  - “Screen **insider trades** across all tickers (limit 50).”
  - “Screen **LinkedIn data** for **US** region stocks.”
  - “What are the **most mentioned tickers** on **Reddit** right now?”

- **Availability**
  - “Which **markets** are available?”
  - “List **tickers** in the **daily** predictions universe.”
  - “Show available **regions** and their markets.”

> **Notes**
>
> - Date format: `YYYY-MM-DD`.
> - Time-series endpoints return the **most recent N** points by default—say “limit 200” to get more.
> - Predictions horizon: **daily** (10-day) or **monthly** (12-month).
> - Say “**as CSV**” to receive CSV instead of JSON.
> - No need to specify a market—just use the ticker symbol directly.

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

© 2026 FinBrain Technologies — Built with ❤️ for the quant community.
