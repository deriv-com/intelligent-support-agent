# Quick Start Guide

## Project Overview
Intelligent Support Agent: AI-powered customer support system using Llama 2, Qdrant, and LangChain.

## Quick Setup
```bash
# 1. Clone and setup
git clone <repository-url>
cd intelligent-support-agent

# 2. Set up environment
cp .env.app.example .env.app
cp .env.postgres.example .env.postgres
cp .env.redis.example .env.redis
cp .env.qdrant.example .env.qdrant

# 3. Install dev tools
pip install pre-commit
pre-commit install

# 4. Start services
docker compose up -d

# 5. Start monitoring (optional)
docker compose -f docker-compose.monitoring.yml up -d
```

## Key Components
- API: FastAPI (port 8000)
- LLM: Ollama/Llama 2
- Vector DB: Qdrant
- Storage: Redis + PostgreSQL

## Essential Commands
```bash
# Development
docker compose up -d           # Start services
docker compose logs -f        # Watch logs
docker compose ps             # Check status

# Testing
docker compose --profile test up test  # Run tests

# Monitoring
open http://localhost:3000    # Grafana (admin/admin)
```

## Key Files
- `src/main.py`: API endpoints
- `src/llm_chain/`: LLM integration
- `src/mcp/`: Context management
- `src/vectorstore/`: Vector search

## Documentation
- README.md: Project overview
- CONTRIBUTING.md: Development guidelines
- docs/HANDOVER.md: Detailed documentation
- context/: Business context

## Development Workflow
1. Write tests first (TDD)
2. Make minimal changes
3. Run pre-commit checks
4. Submit PR

## Common Tasks

### Testing
```bash
# Run specific test file
docker compose --profile test run test pytest tests/test_mcp.py

# Run marked tests
docker compose --profile test run test pytest -m "not slow"

# Generate coverage
docker compose --profile test run test pytest --cov-report=html
```

### Database Operations
```bash
# PostgreSQL shell
docker compose exec postgres psql -U postgres -d support_agent

# Redis CLI
docker compose exec redis redis-cli

# Clear Redis cache
docker compose exec redis redis-cli FLUSHALL
```

### API Usage
```bash
# Basic query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How do I make a deposit?",
    "session_id": "test123"
  }'

# Follow-up query (uses previous context)
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What payment methods are supported?",
    "session_id": "test123"
  }'

# Health check
curl http://localhost:8000/health
```

### Model Management
```bash
# List available models
docker compose exec ollama ollama list

# Pull specific model version
docker compose exec ollama ollama pull llama2:7b

# Check model status
docker compose exec ollama ollama show llama2
```

### Troubleshooting
1. **Services Won't Start**
   ```bash
   # Check logs
   docker compose logs --tail=100
   
   # Rebuild services
   docker compose build --no-cache
   ```

2. **GPU Issues**
   ```bash
   # Check GPU status
   nvidia-smi
   
   # Verify Docker GPU access
   docker compose exec ollama nvidia-smi
   ```

3. **API Issues**
   ```bash
   # Check API health
   curl http://localhost:8000/health
   
   # Watch API logs
   docker compose logs -f app
   ```

4. **Database Issues**
   ```bash
   # Check PostgreSQL connection
   docker compose exec postgres pg_isready
   
   # Check Redis connection
   docker compose exec redis redis-cli ping
   ```

## Development Tips
1. **Testing**
   - Write tests before implementation
   - Use appropriate markers (unit/integration)
   - Check coverage reports

2. **Code Quality**
   - Run pre-commit hooks before committing
   - Follow type hints strictly
   - Update documentation

3. **Monitoring**
   - Check Grafana dashboards regularly
   - Monitor GPU usage
   - Watch error rates

## Need Help?
1. Check HANDOVER.md for detailed docs
2. Review test cases for examples
3. Monitor Grafana dashboards
4. Check logs for issues

## Next Steps
1. Review codebase
2. Run local setup
3. Execute test suite
4. Check monitoring
