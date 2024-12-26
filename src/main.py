import logging
import uuid
from typing import Optional, Dict
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from contextlib import asynccontextmanager

from .config import Config
from .vectorstore import VectorStore
from .mcp import ModelContextProtocol
from .llm_chain import PaymentSupportChain

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    context_size: Optional[int] = 5

class QueryResponse(BaseModel):
    session_id: str
    response: str

class PaymentSupportSystem:
    def __init__(self):
        try:
            self.config = Config()
            self.vector_store = VectorStore(self.config)
            self.mcp = ModelContextProtocol()
            self.llm_chain = PaymentSupportChain(self.config)
            logger.info("Payment Support System initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Payment Support System: {str(e)}")
            raise

    async def process_query(
        self,
        session_id: str,
        query: str,
        context_size: int = 5
    ) -> str:
        try:
            logger.info(f"Processing query for session {session_id}: {query}")

            # Get relevant documents
            relevant_docs = self.vector_store.search(query, limit=context_size)
            logger.info(f"Found {len(relevant_docs)} relevant documents")

            # Get conversation history
            conversation_history = self.mcp.get_context(session_id)

            # Generate response
            response = self.llm_chain.generate_response(
                context=relevant_docs,
                conversation_history=conversation_history,
                question=query
            )

            # Update conversation history
            self.mcp.add_message(session_id, "user", query)
            self.mcp.add_message(session_id, "assistant", response)

            logger.info(f"Successfully processed query for session {session_id}")
            return response
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise RuntimeError(f"Failed to process query: {str(e)}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        app.state.support_system = PaymentSupportSystem()
        logger.info("Application startup complete")
        yield
    except Exception as e:
        logger.error(f"Application startup failed: {str(e)}")
        raise
    finally:
        # Cleanup
        logger.info("Application shutdown")

app = FastAPI(lifespan=lifespan)

async def get_support_system() -> PaymentSupportSystem:
    return app.state.support_system

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(
    request: QueryRequest,
    support_system: PaymentSupportSystem = Depends(get_support_system)
):
    try:
        session_id = request.session_id or str(uuid.uuid4())
        response = await support_system.process_query(
            session_id=session_id,
            query=request.query,
            context_size=request.context_size
        )
        return QueryResponse(session_id=session_id, response=response)
    except Exception as e:
        logger.error(f"Error in query endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
