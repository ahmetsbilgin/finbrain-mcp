# Docker Guide for FinBrain MCP

## Building the Docker Image

### Prerequisites

- Docker Desktop installed and running
- FinBrain API key

### Build the Image

```bash
docker build -t finbrain-mcp:latest .
```

### Test the Image Locally

Test with your API key:

```bash
docker run --rm -e FINBRAIN_API_KEY="your_api_key_here" finbrain-mcp:latest
```

The container will start the MCP server using stdio transport.

## Docker Image Details

### Image Characteristics

- **Base**: Python 3.11-slim
- **Size**: Optimized with multi-stage build (~150MB)
- **Security**: Runs as non-root user (mcpuser)
- **Transport**: stdio (required for MCP)

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `FINBRAIN_API_KEY` | Yes | Your FinBrain API key |

### Health Check

The image includes a health check that verifies the Python package is installed correctly:

```bash
docker ps  # Check HEALTH status
```

## Using with Docker MCP Catalog

Once submitted and approved, the image will be available as:

```text
mcp/finbrain-mcp
```

Users can then pull and run it via:

- Docker Desktop MCP Toolkit
- Docker Hub
- Docker CLI

## Local Development

For local development with Docker:

```bash
# Build
docker build -t finbrain-mcp:dev .

# Run with environment file
docker run --rm --env-file .env finbrain-mcp:dev
```

Create a `.env` file (don't commit it!):

```env
FINBRAIN_API_KEY=your_key_here
```

## Troubleshooting

### Container exits immediately

- Ensure Docker Desktop is running
- Check that FINBRAIN_API_KEY is set
- View logs: `docker logs <container_id>`

### Permission errors

- The container runs as user `mcpuser` (UID 1000)
- Verify file permissions if mounting volumes

### Connection issues

- MCP uses stdio transport
- Ensure client is configured to connect via stdio
- Check container logs for errors

## Security Notes

- Never commit API keys to the repository
- Use Docker secrets or environment variables for sensitive data
- The image runs as non-root for security
- Consider using Docker scan: `docker scan finbrain-mcp:latest`
