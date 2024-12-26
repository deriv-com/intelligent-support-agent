"""Common test fixtures and utilities."""
import pytest
from unittest.mock import Mock
from src.config import Config

@pytest.fixture
def mock_config():
    """Create a mock configuration for testing."""
    config = Mock(spec=Config)
    config.QDRANT_HOST = "qdrant"
    config.QDRANT_PORT = 6333
    config.COLLECTION_NAME = "test_collection"
    config.EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    config.OLLAMA_BASE_URL = "http://ollama:11434"
    config.LLM_MODEL = "llama2"
    return config

@pytest.fixture
def mock_collection():
    """Create a mock Qdrant collection."""
    collection = Mock()
    collection.name = "test_collection"
    return collection

@pytest.fixture
def mock_collections_response():
    """Create a mock Qdrant collections response."""
    response = Mock()
    response.collections = []
    return response

@pytest.fixture
def mock_qdrant_client(mock_collections_response):
    """Create a mock Qdrant client with basic setup."""
    client = Mock()
    client.get_collections.return_value = mock_collections_response
    return client

@pytest.fixture
def sample_documents():
    """Create sample documents for testing."""
    return [
        {
            "title": "Test Document 1",
            "content": "This is a test document about payments",
            "category": "test"
        },
        {
            "title": "Test Document 2",
            "content": "Another test document about transfers",
            "category": "test"
        }
    ]

@pytest.fixture
def sample_embeddings():
    """Create sample embeddings for testing."""
    return [[0.1, 0.2], [0.3, 0.4]]

def assert_mock_calls(mock_obj, expected_calls, msg=None):
    """Helper function to assert mock calls with better error messages."""
    actual_calls = mock_obj.mock_calls
    assert len(actual_calls) == len(expected_calls), (
        f"{msg or 'Incorrect number of calls'}\n"
        f"Expected: {expected_calls}\n"
        f"Got: {actual_calls}"
    )
    for actual, expected in zip(actual_calls, expected_calls):
        assert actual == expected, (
            f"{msg or 'Incorrect call'}\n"
            f"Expected: {expected}\n"
            f"Got: {actual}"
        )
