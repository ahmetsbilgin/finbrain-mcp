# Multi-stage build for optimal image size
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install build dependencies including git (needed for setuptools-scm)
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy project files
COPY pyproject.toml ./
COPY README.md ./
COPY LICENSE ./
COPY src/ ./src/
COPY .git/ ./.git/

# Install the package
RUN pip install --no-cache-dir .

# Final stage - minimal runtime image
FROM python:3.11-slim

# Create non-root user for security
RUN useradd -m -u 1000 -s /bin/bash mcpuser

# Set working directory
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/finbrain-mcp /usr/local/bin/finbrain-mcp

# Switch to non-root user
USER mcpuser

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check (optional - checks if the CLI is available)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import finbrain_mcp; print('OK')" || exit 1

# MCP servers use stdio transport - run the server
ENTRYPOINT ["finbrain-mcp"]
