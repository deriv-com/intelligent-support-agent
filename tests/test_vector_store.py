import pytest
import numpy as np
from unittest.mock import Mock, patch
from src.vectorstore.vector_store import VectorStore
from qdrant_client.models import Record

@patch('src.vectorstore.vector_store.QdrantClient')
@patch('src.vectorstore.vector_store.SentenceTransformer')
def test_vector_store_initialization_new_collection(mock_transformer, mock_qdrant, mock_config, mock_qdrant_client):
    # Arrange
    mock_qdrant.return_value = mock_qdrant_client

    # Act
    vector_store = VectorStore(mock_config)

    # Assert
    mock_qdrant.assert_called_once_with(
        host=mock_config.QDRANT_HOST,
        port=mock_config.QDRANT_PORT
    )
    mock_transformer.assert_called_once_with(mock_config.EMBEDDING_MODEL)
    mock_qdrant_client.create_collection.assert_called_once()

@patch('src.vectorstore.vector_store.QdrantClient')
@patch('src.vectorstore.vector_store.SentenceTransformer')
def test_vector_store_initialization_existing_collection(
    mock_transformer, mock_qdrant, mock_config, mock_collection, mock_collections_response
):
    # Arrange
    mock_collections_response.collections = [mock_collection]
    mock_client = Mock()
    mock_client.get_collections.return_value = mock_collections_response
    mock_qdrant.return_value = mock_client

    # Act
    vector_store = VectorStore(mock_config)

    # Assert
    mock_client.create_collection.assert_not_called()

@pytest.fixture
def mock_embeddings():
    """Mock embeddings as numpy arrays."""
    return np.array([[0.1, 0.2], [0.3, 0.4]])

@patch('src.vectorstore.vector_store.QdrantClient')
@patch('src.vectorstore.vector_store.SentenceTransformer')
def test_add_documents(
    mock_transformer, mock_qdrant, mock_config, mock_qdrant_client, sample_documents, mock_embeddings
):
    # Arrange
    mock_qdrant.return_value = mock_qdrant_client
    mock_transformer.return_value.encode.return_value = mock_embeddings
    vector_store = VectorStore(mock_config)

    # Act
    vector_store.add_documents(sample_documents)

    # Assert
    mock_transformer.return_value.encode.assert_called_once()
    mock_qdrant_client.upload_records.assert_called_once()

    # Verify records format
    call_args = mock_qdrant_client.upload_records.call_args[1]
    records = call_args['records']
    assert isinstance(records[0], Record)
    assert isinstance(records[0].vector, list)

@patch('src.vectorstore.vector_store.QdrantClient')
@patch('src.vectorstore.vector_store.SentenceTransformer')
def test_search(mock_transformer, mock_qdrant, mock_config, mock_qdrant_client):
    # Arrange
    mock_qdrant.return_value = mock_qdrant_client
    # Mock embedding as numpy array since VectorStore expects tolist() method
    mock_embedding = np.array([0.1, 0.2])
    mock_transformer.return_value.encode.return_value = mock_embedding
    mock_qdrant_client.search.return_value = [Mock(payload={"content": "Test response"})]
    vector_store = VectorStore(mock_config)

    # Act
    results = vector_store.search("test query")

    # Assert
    assert len(results) == 1
    mock_transformer.return_value.encode.assert_called_once_with("test query")
    mock_qdrant_client.search.assert_called_once()

    # Verify search vector format
    call_args = mock_qdrant_client.search.call_args[1]
    assert isinstance(call_args['query_vector'], list)
    assert call_args['query_vector'] == mock_embedding.tolist()

@patch('src.vectorstore.vector_store.QdrantClient')
@patch('src.vectorstore.vector_store.SentenceTransformer')
def test_error_handling(mock_transformer, mock_qdrant, mock_config, mock_qdrant_client):
    # Arrange
    mock_qdrant_client.get_collections.side_effect = Exception("Connection error")
    mock_qdrant.return_value = mock_qdrant_client

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        VectorStore(mock_config)
    assert "Connection error" in str(exc_info.value)

@patch('src.vectorstore.vector_store.QdrantClient')
@patch('src.vectorstore.vector_store.SentenceTransformer')
def test_search_with_empty_results(mock_transformer, mock_qdrant, mock_config, mock_qdrant_client):
    # Arrange
    mock_qdrant.return_value = mock_qdrant_client
    mock_qdrant_client.search.return_value = []  # Empty search results
    mock_embedding = np.array([0.1, 0.2])
    mock_transformer.return_value.encode.return_value = mock_embedding
    vector_store = VectorStore(mock_config)

    # Act
    results = vector_store.search("test query")

    # Assert
    assert isinstance(results, list)
    assert len(results) == 0
    mock_qdrant_client.search.assert_called_once()
