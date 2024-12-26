# Build stage
FROM python:3.9-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.9-slim

WORKDIR /app

# Create non-root user first
RUN useradd -m -u 1000 appuser

# Copy only the necessary files from builder
COPY --from=builder /usr/local /usr/local
COPY src/ ./src/
COPY scripts/ ./scripts/

# Create required directories
RUN mkdir -p /app/data

# Set Python path
ENV PYTHONPATH=/app

# Default environment variables
ENV QDRANT_HOST=qdrant \
    QDRANT_PORT=6333 \
    OLLAMA_BASE_URL=http://ollama:11434

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set permissions after all files are copied and directories created
RUN chown -R appuser:appuser /app && \
    chmod -R 755 /usr/local/bin && \
    chmod -R 755 /app/src && \
    chmod -R 755 /app/scripts && \
    chmod -R 777 /app/data

USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
