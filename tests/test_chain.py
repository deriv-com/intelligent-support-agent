"""Tests for the LangChain integration."""
import pytest
from unittest.mock import Mock, patch, call
from src.llm_chain.chain import PaymentSupportChain
from src.mcp.protocol import Message

@pytest.fixture
def mock_llm_response():
    """Sample LLM response with help center link."""
    return "This is a test response that includes help.deriv.com/payments/card-payments"

@pytest.fixture
def mock_llm_chain():
    """Mock LangChain LLMChain."""
    chain = Mock()
    chain.run.return_value = "Test response"
    return chain

@pytest.fixture
def sample_context():
    """Sample context documents."""
    return [
        {
            "title": "Card Payment Issues",
            "content": "Common reasons for card payment failures include insufficient funds. More info at help.deriv.com/payments/card-payments",
            "category": "card_payments"
        },
        {
            "title": "Bank Transfer Delays",
            "content": "Bank transfers may be delayed due to verification. Check help.deriv.com/payments/bank-transfers",
            "category": "bank_transfers"
        }
    ]

@patch('src.llm_chain.chain.LLMChain')
@patch('src.llm_chain.chain.Ollama')
def test_chain_initialization(mock_ollama, mock_llm_chain, mock_config):
    """Test PaymentSupportChain initialization."""
    # Arrange
    mock_llm = Mock()
    mock_ollama.return_value = mock_llm
    mock_chain = Mock()
    mock_llm_chain.return_value = mock_chain

    # Act
    chain = PaymentSupportChain(mock_config)

    # Assert
    mock_ollama.assert_called_once_with(
        base_url=mock_config.OLLAMA_BASE_URL,
        model=mock_config.LLM_MODEL
    )
    mock_llm_chain.assert_called_once()
    assert chain.chain == mock_chain

@patch('src.llm_chain.chain.LLMChain')
@patch('src.llm_chain.chain.Ollama')
def test_generate_response(
    mock_ollama, mock_llm_chain, mock_config, sample_context, mock_llm_response
):
    """Test response generation with context and history."""
    # Arrange
    mock_chain = Mock()
    mock_chain.run.return_value = mock_llm_response
    mock_llm_chain.return_value = mock_chain

    chain = PaymentSupportChain(mock_config)
    conversation_history = [
        Message(role="user", content="Why did my payment fail?"),
        Message(role="assistant", content="Can you provide more details?")
    ]
    question = "I used a credit card"

    # Act
    response = chain.generate_response(sample_context, conversation_history, question)

    # Assert
    assert isinstance(response, str)
    assert "help.deriv.com/payments" in response
    mock_chain.run.assert_called_once()

@patch('src.llm_chain.chain.LLMChain')
@patch('src.llm_chain.chain.Ollama')
def test_context_formatting(mock_ollama, mock_llm_chain, mock_config, sample_context):
    """Test context document formatting."""
    # Arrange
    mock_chain = Mock()
    mock_llm_chain.return_value = mock_chain
    chain = PaymentSupportChain(mock_config)

    # Act
    formatted_context = chain._format_context(sample_context)

    # Assert
    assert isinstance(formatted_context, str)
    assert "Document 1" in formatted_context
    # Check for content rather than title since we're formatting the content
    assert "insufficient funds" in formatted_context
    assert "help.deriv.com/payments" in formatted_context
    assert "help.deriv.com/payments" in formatted_context

@patch('src.llm_chain.chain.LLMChain')
@patch('src.llm_chain.chain.Ollama')
def test_history_formatting(mock_ollama, mock_llm_chain, mock_config):
    """Test conversation history formatting."""
    # Arrange
    mock_chain = Mock()
    mock_llm_chain.return_value = mock_chain
    chain = PaymentSupportChain(mock_config)

    history = [
        Message(role="user", content="Why did my payment fail?"),
        Message(role="assistant", content="Can you provide more details?"),
        Message(role="user", content="I used a credit card")
    ]

    # Act
    formatted_history = chain._format_history(history)

    # Assert
    assert isinstance(formatted_history, str)
    for msg in history:
        assert msg.content in formatted_history
        assert msg.role.capitalize() in formatted_history

@patch('src.llm_chain.chain.LLMChain')
@patch('src.llm_chain.chain.Ollama')
def test_error_handling(mock_ollama, mock_llm_chain, mock_config):
    """Test error handling in response generation."""
    # Arrange
    mock_chain = Mock()
    mock_chain.run.side_effect = Exception("LLM error")
    mock_llm_chain.return_value = mock_chain

    chain = PaymentSupportChain(mock_config)

    # Act & Assert
    with pytest.raises(RuntimeError) as exc_info:
        chain.generate_response([], [], "test question")
    assert "Failed to generate response" in str(exc_info.value)

@patch('src.llm_chain.chain.LLMChain')
@patch('src.llm_chain.chain.Ollama')
def test_empty_inputs(mock_ollama, mock_llm_chain, mock_config, mock_llm_response):
    """Test handling of empty inputs."""
    # Arrange
    mock_chain = Mock()
    mock_chain.run.return_value = mock_llm_response
    mock_llm_chain.return_value = mock_chain

    chain = PaymentSupportChain(mock_config)

    # Act
    response = chain.generate_response([], [], "test question")

    # Assert
    assert isinstance(response, str)
    assert response == mock_llm_response
    mock_chain.run.assert_called_once()

@patch('src.llm_chain.chain.LLMChain')
@patch('src.llm_chain.chain.Ollama')
def test_prompt_template(mock_ollama, mock_llm_chain, mock_config):
    """Test prompt template configuration."""
    # Arrange
    chain = PaymentSupportChain(mock_config)

    # Assert
    assert "help.deriv.com/payments" in chain.prompt.template
    assert all(var in chain.prompt.input_variables
              for var in ["context", "conversation_history", "question"])
