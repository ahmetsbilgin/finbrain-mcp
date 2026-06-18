# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.4] - 2026-06-18

### Added

- `patent_filings_by_ticker` tool — USPTO granted patents mapped to a single ticker by corporate assignee (patent ID, grant date, title, type, claims, citations, CPC classification, inventors, filing-to-grant time)
- `screener_patent_filings` tool — cross-ticker patent filings screening with summary stats (total patents, total tickers, top CPC sections)
- Integration tests for patent filings (ticker, screener, and tool-level round-trip)

### Fixed

- Screener `summary` block is now populated for `screener_government_contracts` (regression since 0.2.3) and `screener_reddit_mentions` (since 0.2.2) — both previously returned all-`null` summary fields because the SDK unwraps screener responses down to the rows and discards the summary. The adapter now fetches the full envelope so the backend-computed summary is preserved.

### Changed

- Bumped `finbrain-python` dependency from `>=0.2.3` to `>=0.2.5` (required for patent filings endpoints)
- `FBClient` now caches the underlying `finbrain-python` client per API key, so repeated tool calls reuse a single HTTP session/connection pool instead of opening a new one each call
- Strengthened screener integration tests to assert summary *values* (not just key presence), which is what previously masked the empty-summary bug
- Internal cleanup: removed the unused `_make_client` helper from the server entrypoint, documented `latest_slice`'s chronological-ordering assumption, and corrected README inaccuracies (a non-existent `settings.py` in the project tree and the API-key configuration note)

## [0.2.3] - 2026-03-30

### Added

- `government_contracts_by_ticker` tool — U.S. government contract awards (award amount, awarding agency, NAICS classification, dates) for a single ticker
- `screener_government_contracts` tool — cross-ticker government contract screening with summary stats (total contracts, total value)
- Integration tests for government contracts (ticker, screener, and tool-level round-trip)

### Changed

- Bumped `finbrain-python` dependency from `>=0.2.3` to `>=0.2.4` (required for government contracts endpoints)

## [0.2.2] - 2026-03-17

### Added

- `reddit_mentions_by_ticker` tool — Reddit mention counts across subreddits for a single ticker (date, subreddit, mentions)
- `screener_reddit_mentions` tool — cross-ticker Reddit mention screening with per-subreddit breakdown and summary stats

### Changed

- Bumped `finbrain-python` dependency from `>=0.2.1` to `>=0.2.3` (required for Reddit mentions endpoints)

## [0.2.1] - 2026-03-12

### Added

- `corporate_lobbying_by_ticker` tool — corporate lobbying filings (registrant, income, expenses, issue codes, government entities) for a single ticker

### Changed

- Bumped `finbrain-python` dependency from `>=0.2.0` to `>=0.2.1` (required for corporate lobbying endpoint)

## [0.2.0] - 2026-03-10

### Added

- `news_by_ticker` tool — recent news articles with per-article sentiment for a single ticker
- `available_regions` tool — list markets grouped by region
- `recent_news` tool — latest news articles across all tracked stocks
- `recent_analyst_ratings` tool — latest analyst ratings across all tracked stocks
- 9 screener tools for cross-ticker screening:
  - `screener_sentiment`, `screener_analyst_ratings`, `screener_news`
  - `screener_insider_trading`, `screener_house_trades`, `screener_senate_trades`
  - `screener_put_call_ratio`, `screener_linkedin`, `screener_app_ratings`

### Changed

- **BREAKING:** Migrated from FinBrain API v1 to v2
  - The `market` parameter has been removed from all per-symbol tool inputs (`news_sentiment_by_ticker`, `app_ratings_by_ticker`, `analyst_ratings_by_ticker`, `house_trades_by_ticker`, `senate_trades_by_ticker`, `insider_transactions_by_ticker`, `linkedin_metrics_by_ticker`, `options_put_call`)
  - `predictions_by_market` now uses the v2 screener endpoint and accepts optional `market`, `region`, and `prediction_type` parameters instead of a required `market`
  - `insider_transactions_by_ticker` now supports `date_from` and `date_to` parameters
- Upgraded `fastmcp` dependency from v2 to v3
- Upgraded `finbrain-python` dependency from v0.1.x to v0.2.0
- Rewrote all normalizers for v2 response shapes (field renames, restructured data keys, nested objects)
- Updated fake SDK fixtures and all tests for v2 compatibility

## [0.1.6] - 2026-01-07

### Added

- Senate trades API endpoint (`senate_trades_by_ticker`) for US Senator stock transactions
- Python 3.14 to CI test matrix
- Documentation link to official FinBrain MCP page

### Changed

- Updated "US Congress Trades" feature to include both House and Senate disclosures
- README improvements with new Features section and examples

## [0.1.5] - 2025-10-02

### Added

- Docker support with multi-stage Dockerfile for containerized deployment
- Docker usage guide (DOCKER.md)
- CHANGELOG.md to track version history

### Changed

- Documentation improvements and linting

## [0.1.4] - 2025-09-19

### Changed

- Updated VS Code example JSON files
- Improved README with better instructions and examples

## [0.1.3] - 2025-09-19

### Changed

- Updated README with comprehensive instructions and examples
- Replaced pipx with pip in example JSON configurations

## [0.1.2] - 2025-09-19

### Changed

- Updated pyproject.toml configuration
- README documentation improvements

## [0.1.1] - 2025-09-19

### Added

- Dynamic version detection using setuptools-scm with git tags

### Fixed

- Removed unused imports

## [0.1.0] - 2025-09-18

### Added

- Initial release of FinBrain MCP server
- MCP tools for FinBrain datasets:
  - Health check
  - Available markets and tickers
  - Predictions (by market and ticker)
  - News sentiment analysis
  - App ratings
  - Analyst ratings
  - House trades
  - Insider transactions
  - LinkedIn metrics
  - Options put/call ratios
- Support for JSON and CSV output formats
- Data normalization for consistent API responses
- Integration with finbrain-python SDK
- FastMCP-based server implementation
- Comprehensive test suite
- CI/CD with GitHub Actions
- Python 3.10+ support (tested on 3.10, 3.11, 3.12, 3.13)
- Type checking with mypy
- Linting with ruff
- Example configurations for Claude Desktop and VS Code

[0.2.4]: https://github.com/ahmetsbilgin/finbrain-mcp/compare/v0.2.3...v0.2.4
[0.2.3]: https://github.com/ahmetsbilgin/finbrain-mcp/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/ahmetsbilgin/finbrain-mcp/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/ahmetsbilgin/finbrain-mcp/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/ahmetsbilgin/finbrain-mcp/compare/v0.1.6...v0.2.0
[0.1.6]: https://github.com/ahmetsbilgin/finbrain-mcp/compare/v0.1.5...v0.1.6
[0.1.5]: https://github.com/ahmetsbilgin/finbrain-mcp/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/ahmetsbilgin/finbrain-mcp/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/ahmetsbilgin/finbrain-mcp/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/ahmetsbilgin/finbrain-mcp/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/ahmetsbilgin/finbrain-mcp/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/ahmetsbilgin/finbrain-mcp/releases/tag/v0.1.0
