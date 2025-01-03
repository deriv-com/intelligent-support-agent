# Project Handover Document

## Project Overview

### Purpose
The Intelligent Support Agent is an AI-powered customer support automation system designed for Deriv.com's payment support queries. It combines:
- Local LLM inference (Llama 2)
- Semantic search (Qdrant)
- Conversation management
- Context-aware responses

### Business Context
1. **Problem Statement**
   - High volume of payment-related support queries
   - Need for consistent responses
   - Complex context tracking required
   - Multiple payment methods to handle

2. **Solution Approach**
   - Local LLM deployment for data privacy
   - Vector search for relevant documentation
   - Session management for conversation context
   - Hybrid storage for performance and persistence

## Technical Architecture

### Core Components

1. **LLM Service (Ollama)**
   - Uses Llama 2 model
   - Local inference for privacy
   - GPU acceleration supported
   - Location: `src/llm_chain/`

2. **Vector Database (Qdrant)**
   - Stores document embeddings
   - Enables semantic search
   - Rust-based for performance
   - Location: `src/vectorstore/`

3. **Model Context Protocol (MCP)**
   - Manages conversation state
   - Handles session tracking
   - Hybrid storage (Redis + PostgreSQL)
   - Location: `src/mcp/`

4. **API Layer (FastAPI)**
   - RESTful endpoints
   - Session management
   - Request handling
   - Location: `src/main.py`

### Data Flow
1. User sends query → API
2. API retrieves conversation context (MCP)
3. Vector search finds relevant docs (Qdrant)
4. LLM generates response (Ollama)
5. Response stored in context (MCP)
6. Final response sent to user

## Development Environment

### Setup Requirements
1. Install dependencies:
   ```bash
   # Clone repository
   git clone https://github.com/deriv-com/intelligent-support-agent
   cd intelligent-support-agent

   # Set up environment
   cp .env.app.example .env.app
   cp .env.postgres.example .env.postgres
   cp .env.redis.example .env.redis
   cp .env.qdrant.example .env.qdrant

   # Install pre-commit hooks
   pip install pre-commit
   pre-commit install
   ```

1. GPU Support (Optional):

   - Follow NVIDIA setup in README.md
   - Update docker-compose.yml GPU settings

2. Start Services:

   ```bash
   docker compose up -d
   ```

### Development Workflow

1. **Test-Driven Development**
   - Write tests first
   - Implement features
   - Run test suite
   - Location: `tests/`
2. **Code Quality**
   - Pre-commit hooks run:
     - black (formatting)
     - flake8 (linting)
     - mypy (type checking)
     - isort (import sorting)
3. **Documentation**
   - Update README.md for features
   - Add docstrings for public functions
   - Keep architecture diagrams current

## Key Areas of Focus

### Current State

1. **Working Features**
   - Query processing pipeline
   - Conversation context management
   - Semantic search integration
   - GPU acceleration support
   - Session persistence
2. **Recent Changes**
   - Added hybrid storage (Redis + PostgreSQL)
   - Implemented pre-commit hooks
   - Updated documentation
   - Added development guidelines

### Future Development

1. **Planned Features**
   - Enhanced error handling
   - Performance optimizations
   - Additional payment methods support
   - Analytics integration
2. **Known Issues**
   - Monitor Redis memory usage
   - Watch for GPU memory leaks
   - Handle large conversation histories

## Testing Strategy

### Test Categories

1. **Unit Tests**
   - Component-level testing
   - Mocked dependencies
   - Fast execution
2. **Integration Tests**
   - Cross-component testing
   - Database interactions
   - API endpoints
3. **Performance Tests**
   - Response time benchmarks
   - Memory usage monitoring
   - Concurrent request handling

### Running Tests

```bash
# Full test suite
docker compose --profile test up test

# Specific components
docker compose --profile test run test pytest -m vectorstore
docker compose --profile test run test pytest -m mcp
docker compose --profile test run test pytest -m chain
```

## Deployment

### Local Development

```bash
# Start all services
docker compose up -d

# Monitor logs
docker compose logs -f

# Check status
docker compose ps
```

### Production Considerations

1. **Security**
   - Update default passwords
   - Configure proper network settings
   - Enable security features
   - Review logging settings
2. **Performance**
   - Monitor Redis memory
   - Check PostgreSQL connections
   - Watch GPU utilization
   - Scale container resources

## Important Resources

### Documentation

1. **Project**
   - README.md: Main documentation
   - CONTRIBUTING.md: Development guidelines
   - context/: Business context files
2. **External**
   - [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction.html)
   - [Qdrant Documentation](https://qdrant.tech/documentation/)
   - [Ollama Documentation](https://ollama.ai/docs)

### Configuration Files

1. **Development**
   - .pre-commit-config.yaml
   - setup.cfg
   - pyproject.toml
2. **Environment**
   - .env.app.example
   - .env.postgres.example
   - .env.redis.example
   - .env.qdrant.example

## Support and Communication

### Getting Help

1. Check existing documentation in:
   - README.md
   - CONTRIBUTING.md
   - Code comments and docstrings
2. Review test cases for examples:
   - tests/test_chain.py
   - tests/test_mcp.py
   - tests/test_vector_store.py

### Best Practices

1. Follow TDD approach
2. Make targeted changes
3. Update documentation
4. Run full test suite
5. Use pre-commit hooks

## Architectural Decisions

### Key Design Choices

1. **Local LLM vs Cloud Services**
   - Decision: Local Llama 2 via Ollama
   - Rationale:
     * Data privacy for sensitive payment information
     * Lower latency for real-time responses
     * Cost-effective for high volume queries
     * Full control over model behavior

2. **Hybrid Storage Strategy**
   - Decision: Redis + PostgreSQL combination
   - Rationale:
     * Redis for fast access to active sessions
     * PostgreSQL for reliable persistence
     * Automatic fallback mechanism
     * Better scalability and performance

3. **Vector Search Implementation**
   - Decision: Qdrant vector database
   - Rationale:
     * Rust-based for high performance
     * HNSW algorithm for efficient search
     * Good balance of speed and accuracy
     * Active development and community

4. **Model Context Protocol**
   - Decision: Custom MCP implementation
   - Rationale:
     * Flexible conversation management
     * Easy to extend for new features
     * Clear separation of concerns
     * Simplified testing and maintenance

### Technology Stack Decisions

1. **FastAPI Framework**
   - Async support for better performance
   - Built-in OpenAPI documentation
   - Type hints and validation
   - Easy to test and maintain

2. **Docker Containerization**
   - Consistent development environment
   - Easy deployment and scaling
   - Isolated service management
   - GPU support through NVIDIA Container Toolkit

3. **Testing Framework**
   - Pytest for comprehensive testing
   - Containerized test environment
   - Coverage reporting
   - Clear test categories

4. **Development Tools**
   - Pre-commit hooks for quality
   - Black for consistent formatting
   - MyPy for type checking
   - Flake8 for linting

## Next Steps

1. **Immediate Tasks**
   - Review codebase thoroughly
   - Run local development setup
   - Execute test suite
   - Check current issues/tasks
2. **Learning Path**
   - Study architecture diagram
   - Review test cases
   - Examine core components
   - Test API endpoints

## Common Development Scenarios

### 1. Adding New Features

1. **Extending LLM Capabilities**
   ```python
   # Example: Adding new prompt template
   class PaymentSupportChain:
       def __init__(self, config: Config):
           self.prompt = PromptTemplate(
               input_variables=["context", "history", "query"],
               template="""Your new template here"""
           )

1. **Adding API Endpoints**

   ```python
	# Example: New endpoint for session management
   @app.post("/session/clear")
   async def clear_session(
       session_id: str,
       support_system: PaymentSupportSystem = Depends(get_support_system)
   ):
       await support_system.mcp.clear_session(session_id)
       return {"status": "success"}
   ```

2. **Extending Storage**

```python
# Example: Adding new metadata field
class DatabaseConnection:
   def update_session_tags(self, session_id: str, tags: List[str]) -> None:
       with self.get_postgres_connection() as conn:
           with conn.cursor() as cur:
               cur.execute(
                   "UPDATE sessions SET tags = %s WHERE id = %s",
                   (tags, session_id)
               )
```

### 2. Troubleshooting Guide

1. **GPU Issues**

   - Problem: CUDA out of memory

```bash
 # Check GPU memory
 nvidia-smi

# Reduce model size in config
 LLM_MODEL=llama2:7b  # Instead of larger models
```

2. **Database Connectivity**

   - Problem: Redis connection fails

```bash
docker compose logs redis

docker compose exec app ping redis
```

3. **API Performance**

   - Problem: Slow response times

```bash
# Monitor response times
docker compose logs app | grep "Response time"

# Check vector search
docker compose exec app python -m scripts.benchmark_search
```

### 3. Common Tasks

1. **Updating Dependencies**

```bash
# Update requirements
pip-compile requirements.in

# Rebuild containers
docker compose build --no-cache
```

2. **Running Specific Tests**

```bash
# Run single test file
docker compose --profile test run test pytest tests/test_mcp.py

# Run marked tests
docker compose --profile test run test pytest -m "not slow"
```

3. **Database Management**

```bash
# Access PostgreSQL
docker compose exec postgres psql -U postgres -d support_agent

# Monitor Redis
docker compose exec redis redis-cli monitor
```

### 4. Performance Optimization

1. **Vector Search**

```python
# Optimize chunk size
CHUNK_SIZE = 512  # Adjust based on content

# Use efficient search params
search_params = {
   "hnsw_ef": 128,
   "exact": False
}
```

2. **Caching Strategy**

```python
# Implement response cache
@cached(ttl=3600)
async def get_similar_documents(query: str) -> List[Dict]:
   return await vector_store.search(query)
```

3. **Resource Management**

```python
# Configure connection pools
max_connections = min(cpu_count() * 2, 20)
pool = await asyncpg.create_pool(max_size=max_connections)
```

Remember:

- Code quality is priority
- Tests must pass
- Documentation stays current
- Follow TDD approach

## Monitoring and Maintenance

### System Health Monitoring

1. **Service Health Checks**
```bash
# Check all services
curl http://localhost:8000/health

# Individual components
docker compose ps
docker compose logs --tail=100 app
docker compose logs --tail=100 ollama
```

2. **Resource Monitoring**
```bash
# GPU Utilization
watch -n1 nvidia-smi

# Container Stats
docker stats

# Database Connections
docker compose exec postgres psql -U postgres -c 'SELECT count(*) FROM pg_stat_activity;'
```

3. **Log Analysis**
```bash
# Error tracking
docker compose logs | grep ERROR

# Response times
docker compose logs app | grep "Response time"

# LLM performance
docker compose logs ollama | grep "inference time"
```

### Regular Maintenance Tasks

1. **Database Maintenance**
```bash
# PostgreSQL vacuum
docker compose exec postgres vacuumdb -U postgres -d support_agent --analyze

# Redis memory check
docker compose exec redis redis-cli info memory

# Qdrant optimization
curl -X POST http://localhost:6333/collections/support_docs/optimize
```

2. **Model Updates**
```bash
# Update Llama model
docker compose exec ollama ollama pull llama2:latest

# Verify model
docker compose exec ollama ollama list
```

3. **Backup Procedures**
```bash
# PostgreSQL backup
docker compose exec postgres pg_dump -U postgres support_agent > backup.sql

# Redis backup
docker compose exec redis redis-cli save

# Vector DB backup
curl -X POST http://localhost:6333/collections/support_docs/backup
```

### Performance Tuning

1. **Response Time Optimization**
   - Monitor p95 latency
   - Track vector search times
   - Measure LLM inference
   - Optimize database queries

2. **Resource Allocation**
   - Adjust container limits
   - Configure connection pools
   - Set appropriate cache TTLs
   - Monitor memory usage

3. **Load Testing**
```bash
# Run load tests
docker compose --profile test run test pytest tests/performance/test_load.py

# Monitor during load
docker stats
```

### Alert Thresholds

1. **Critical Alerts**
   - Response time > 2s
   - GPU memory > 90%
   - Database connections > 80%
   - Error rate > 1%

2. **Warning Alerts**
   - Response time > 1s
   - GPU memory > 70%
   - Database connections > 60%
   - Redis memory > 70%

3. **Monitoring Setup**
```bash
# Set up monitoring stack
docker compose -f docker-compose.monitoring.yml up -d

# Access monitoring dashboards
Grafana: http://localhost:3000 (admin/admin)
Prometheus: http://localhost:9090
cAdvisor: http://localhost:8080
```

   Key Metrics Monitored:
   - Response times (p95, p99)
   - Request rates
   - GPU utilization
   - Memory usage
   - Error rates
   - Database connections
   - Cache hit rates

   Dashboard Features:
   - Real-time metrics
   - Historical data
   - Performance trends
   - Resource utilization
   - System health indicators

   Alert Configuration:
   - Response time thresholds
   - Error rate limits
   - Resource usage warnings
   - System health checks

Remember:
- Code quality is priority
- Tests must pass
- Documentation stays current
- Follow TDD approach
- Monitor system health
- Regular maintenance is key
- Check monitoring dashboards daily
- Review and adjust alert thresholds
