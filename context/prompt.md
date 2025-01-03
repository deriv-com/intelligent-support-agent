You are a Python developer building a payment support automation system using LangChain, LLMs, Vector Databases, and Model Context Protocol (MCP). The system helps answer customer queries related to payment failures in a trading platform.

Key components and requirements (prioritizing open-source solutions): 

1. Vector Database: Qdrant (open source, Rust-based) or alternatives like Milvus/ChromaDB
2. LLM: Llama 2 via Ollama (open source) or alternatives like Mistral/Phi-2 
3. Embeddings: sentence-transformers (HuggingFace) or BGE Embeddings 
4. Orchestration: LangChain (open source) or LlamaIndex 
5. Local deployment using Docker/docker-compose 
6. Built with Python 
7. MCP for conversation context management

Core functionality: 

1. Stores and retrieves payment-related documentation
2. Maintains conversation context using MCP
3. Generates relevant responses using locally deployed LLM 
4. Handles user sessions and conversation history 
5. Implements vector similarity search for finding relevant documentation

Project structure: 

- Docker setup for vector DB and LLM
- Vector store handling using LangChain integration
- MCP implementation for context management
- LLM chain for response generation
- Test payment documentation generation
- Main application logic for query handling

The system should be designed to be extensible and maintainable, with clear separation of concerns between components. Focus on implementing robust error handling and clean code practices. All components should preferably use open-source solutions to avoid vendor lock-in and maintain full control over deployment.