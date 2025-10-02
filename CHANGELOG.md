# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.1.5]: https://github.com/ahmetsbilgin/finbrain-mcp/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/ahmetsbilgin/finbrain-mcp/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/ahmetsbilgin/finbrain-mcp/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/ahmetsbilgin/finbrain-mcp/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/ahmetsbilgin/finbrain-mcp/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/ahmetsbilgin/finbrain-mcp/releases/tag/v0.1.0
