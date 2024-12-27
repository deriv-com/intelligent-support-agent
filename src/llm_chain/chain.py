from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from typing import List, Dict
import logging
from ..config import Config
from ..mcp.protocol import Message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PaymentSupportChain:
    def __init__(self, config: Config):
        try:
            self.llm = Ollama(
                base_url=config.OLLAMA_BASE_URL,
                model=config.LLM_MODEL
            )

            self.prompt = PromptTemplate(
                input_variables=["context", "conversation_history", "question"],
                template="""You are a helpful payment support assistant. Use the following context and conversation history to answer the user's question. Always include relevant help center links from the context in your response.

Context:
{context}

Conversation History:
{conversation_history}

User Question: {question}

Important: Make sure to include the relevant help.deriv.com/payments URL from the context in your response.

Assistant Response:"""
            )

            self.chain = (
                RunnablePassthrough() | self.prompt | self.llm | StrOutputParser()
            )
            logger.info(f"Initialized PaymentSupportChain with model {config.LLM_MODEL}")
        except Exception as e:
            logger.error(f"Failed to initialize PaymentSupportChain: {str(e)}")
            raise

    def generate_response(
        self,
        context: List[Dict],
        conversation_history: List[Message],
        question: str
    ) -> str:
        try:
            logger.info(f"Generating response for question: {question}")
            context_str = self._format_context(context)
            history_str = self._format_history(conversation_history)

            response = self.chain.invoke({
                "context": context_str,
                "conversation_history": history_str,
                "question": question
            })

            logger.info("Successfully generated response")
            return response
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise RuntimeError(f"Failed to generate response: {str(e)}")

    def _format_context(self, context: List[Dict]) -> str:
        """Helper method to format context documents into a string."""
        try:
            return "\n\n".join([
                f"Document {i+1}:\n{doc['content']}"
                for i, doc in enumerate(context)
            ])
        except Exception as e:
            logger.error(f"Error formatting context: {str(e)}")
            raise ValueError(f"Invalid context format: {str(e)}")

    def _format_history(self, history: List[Message]) -> str:
        """Helper method to format conversation history into a string."""
        try:
            return "\n".join([
                f"{msg.role.capitalize()}: {msg.content}"
                for msg in history
            ])
        except Exception as e:
            logger.error(f"Error formatting history: {str(e)}")
            raise ValueError(f"Invalid history format: {str(e)}")
