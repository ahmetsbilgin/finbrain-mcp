# FinBrain MCP&nbsp;<!-- omit in toc -->

[![PyPI version](https://img.shields.io/pypi/v/finbrain-mcp.svg)](https://pypi.org/project/finbrain-mcp/)
[![CI](https://github.com/ahmetsbilgin/finbrain-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/ahmetsbilgin/finbrain-mcp/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)


A **Model Context Protocol (MCP)** server that exposes FinBrain datasets to AI clients (Claude Desktop, VS Code MCP extensions, etc.) via simple tools.  
Backed by the official **`finbrain-python`** SDK.

-   Package name: **`finbrain-mcp`**
    
-   CLI entrypoints: **`finbrain-mcp`**, **`finbrain-mcp-login`**
    

----------

## What you get

-   ⚡️ **Local** MCP server (no proxying) using your **own FinBrain API key**
    
-   🧰 Tools (JSON by default, CSV optional) with paging
    
    -   `health`
        
    -   `available_markets`, `available_tickers`
        
    -   `predictions_by_market`, `predictions_by_ticker`
        
    -   `news_sentiment_by_ticker`
        
    -   `app_ratings_by_ticker`
        
    -   `analyst_ratings_by_ticker`
        
    -   `house_trades_by_ticker`
        
    -   `insider_transactions_by_ticker`
        
    -   `linkedin_metrics_by_ticker`
        
    -   `options_put_call`
        
-   🧹 Consistent, model-friendly shapes (we normalize raw API responses)
    
-   🔑 Multiple ways to provide your API key: env var, file, or OS keyring
    

----------

## Install

### Option A — Isolated install (recommended)

```
# macOS/Linux
pipx install finbrain-mcp
pipx upgrade finbrain-mcp
```

```
# from repo root
python -m venv .venv
source .venv/bin/activate              # Windows: .\.venv\Scripts\activate
pip install -e ".[dev]"
```

> Keep **pipx** (prod) and your **venv** (dev) separate to avoid path mix-ups.

----------

## Configure your FinBrain API key

### A) In your MCP client config (recommended / most reliable)

Put the key directly in the MCP server entry your client uses (Claude Desktop or a VS Code MCP extension). This guarantees the launched server sees it, even if system env vars aren’t picked up.

#### Claude Desktop (pip/pipx install):
```
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

```
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

-   If installed (pipx/pip):
    
    `finbrain-mcp` 
    
-   From a dev venv:
    
    `python -m finbrain_mcp.server` 
    

Quick health check without an MCP client:

```
python - <<'PY'
import json
from finbrain_mcp.tools.health import health
print(json.dumps(health(), indent=2))
PY
```

----------

## Connect an AI client

### Claude Desktop

Edit your config:

-   Windows: `%APPDATA%\Claude\claude_desktop_config.json`
    
-   macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
    
-   Linux: `~/.config/Claude/claude_desktop_config.json`
    

**Pipx install (published package):**

```
{
  "mcpServers": {
    "finbrain": {
      "command": "finbrain-mcp",
      "env": { "FINBRAIN_API_KEY": "YOUR_KEY" }
    }
  }
}

```

**Dev venv (run the module explicitly):**

```
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

> Tip: You can omit the `env` block if you used `finbrain-mcp-login`.  
> After editing, **quit & reopen Claude**.

### VS Code (MCP-capable extensions)

Most accept a similar JSON:

```
{
  "mcpServers": {
    "finbrain": {
      "command": "finbrain-mcp",
      "env": { "FINBRAIN_API_KEY": "YOUR_KEY" }
    }
  }
}
```

----------

## Using the tools

All tools return JSON by default and support paging; many also support CSV via `format="csv"`.

### Availability

-   `available_markets() → list[str]`
    
-   `available_tickers({ "dataset": "predictions" }) → [{"ticker": "...", "name": "...", "market": "..."}]`
    

### Predictions

- `predictions_by_market({ "market": "S&P 500", "limit": 100 })`  
  Returns the **latest** rows (sorted by `last_update`) with flat fields:
  `expected_short|mid|long`, `sentiment_score`, `last_update`, `type`, …

- `predictions_by_ticker({ "ticker": "AMZN", "prediction_type": "daily" })`  
  Or `"monthly"` for 12-month horizon. Returns metadata +  
  `series: [{date, mid, low, high}]` and `sentiment: [{date, score}]`.
        

### Sentiment

-   `news_sentiment_by_ticker({ "market": "S&P 500", "ticker": "AMZN", "limit": 30 })`
    
    -   `series: [{date, score}]`
        

### App Ratings

-   `app_ratings_by_ticker({ "market": "S&P 500", "ticker": "AMZN", "limit": 50 })`
    
    -   `series: [{date, play_store_score, play_store_ratings_count, app_store_score, app_store_ratings_count, play_store_install_count}]`
        

### Analyst Ratings

-   `analyst_ratings_by_ticker({ "market": "S&P 500", "ticker": "AMZN" })`
    
    -   `series: [{date, rating_type, institution, signal, target_price_from, target_price_to, target_price_raw}]`
        

### House Trades

-   `house_trades_by_ticker({ "market": "S&P 500", "ticker": "AMZN" })`
    
    -   `series: [{date, representative, trade_type, amount_min, amount_max, amount_exact, amount_raw}]`
        

### Insider Transactions

-   `insider_transactions_by_ticker({ "market": "S&P 500", "ticker": "AMZN" })`
    
    -   `series: [{date, date_raw, insider_name, relationship, transaction_type, price, shares, usd_value, total_shares, sec_form4_date, sec_form4_datetime, sec_form4_link}]`
        

### LinkedIn

-   `linkedin_metrics_by_ticker({ "market": "S&P 500", "ticker": "AMZN" })`
    
    -   `series: [{date, employee_count, followers_count}]`
        

### Options (Put/Call)

-   `options_put_call({ "market": "S&P 500", "ticker": "AMZN" })`
    
    -   `series: [{date, put_call_ratio, call_count, put_count}]`
        

> Most tools accept `offset` & `limit`, and `format: "csv"` to get CSV text of the sliced series.

----------

## Development

```
# setup
python -m venv .venv
source .venv/bin/activate # Windows: .\.venv\Scripts\activate
pip install -e ".[dev]"  # run tests pytest -q
```

### Project structure (high level)

```
src/finbrain_mcp/
  server.py # MCP server entrypoint
  registry.py # FastMCP instance
  client_adapter.py # wraps finbrain-python and normalizes outputs
  auth.py # resolves API key (env/file/keyring)
  utils.py # generic helpers (paging, CSV, DF->records) normalizers/ # endpoint-specific shapers
tools/ # MCP tool functions (registered & testable)
tests/ # pytest suite with a fake SDK
examples/ # sample client configs
```

----------

## Troubleshooting

-   **`ENOENT`** (can’t start server)
    
    -   Wrong path in client config. Use the venv’s **exact** path:
        
        -   `…\.venv\Scripts\python.exe` + `["-m","finbrain_mcp.server"]`, or
            
        -   `…\.venv\Scripts\finbrain-mcp.exe`
            
-   **`FinBrain API key not configured`**
    
    -   Put `FINBRAIN_API_KEY` in the client’s `env` block **or**
        
    -   Run `finbrain-mcp-login` (install `keyring` if missing) **or**
        
    -   `setx FINBRAIN_API_KEY "YOUR_KEY"` and fully restart the client.
        
-   **Mixing dev & prod installs**
    
    -   Keep **pipx** (prod) and **venv** (dev) separate.
        
    -   In configs, point to one or the other—not both.
        

----------

## License

MIT (see `LICENSE`).

----------

## Acknowledgements

-   Built on Model Context Protocol and **FastMCP**.
    
-   Uses the official **`finbrain-python`** SDK.
----------

© 2025 FinBrain Technologies — Built with ❤️ for the quant community.