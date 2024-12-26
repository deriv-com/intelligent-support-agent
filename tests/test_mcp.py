import pytest
from src.mcp.protocol import ModelContextProtocol, Message, Conversation

@pytest.fixture
def mcp():
    return ModelContextProtocol()

@pytest.fixture
def conversation_messages():
    return [
        Message(role="user", content="Why did my payment fail?"),
        Message(role="assistant", content="There could be several reasons. Can you tell me more about the payment method?"),
        Message(role="user", content="I used a credit card"),
        Message(role="assistant", content="Let me check the common issues with credit card payments."),
        Message(role="user", content="It says insufficient funds"),
    ]

def test_create_session(mcp):
    """Test session creation and initialization."""
    session_id = "test_session"

    mcp.create_session(session_id)

    assert session_id in mcp.conversations
    assert len(mcp.conversations[session_id].messages) == 0

def test_add_message_new_session(mcp):
    """Test adding a message to a new session."""
    session_id = "new_session"
    role = "user"
    content = "Test message"

    mcp.add_message(session_id, role, content)

    messages = mcp.conversations[session_id].messages
    assert len(messages) == 1
    assert messages[0].role == role
    assert messages[0].content == content

def test_add_message_existing_session(mcp):
    """Test adding multiple messages to an existing session."""
    session_id = "test_session"
    messages = [
        ("user", "First message"),
        ("assistant", "First response"),
        ("user", "Second message")
    ]

    for role, content in messages:
        mcp.add_message(session_id, role, content)

    assert len(mcp.conversations[session_id].messages) == len(messages)
    for i, (role, content) in enumerate(messages):
        assert mcp.conversations[session_id].messages[i].role == role
        assert mcp.conversations[session_id].messages[i].content == content

def test_get_context_empty_session(mcp):
    """Test getting context from a nonexistent session."""
    context = mcp.get_context("nonexistent_session")

    assert isinstance(context, list)
    assert len(context) == 0

def test_get_context_with_messages(mcp, conversation_messages):
    """Test getting full context from a session with messages."""
    session_id = "test_session"
    for msg in conversation_messages:
        mcp.add_message(session_id, msg.role, msg.content)

    context = mcp.get_context(session_id)

    assert len(context) == len(conversation_messages)
    for original, retrieved in zip(conversation_messages, context):
        assert retrieved.role == original.role
        assert retrieved.content == original.content

def test_get_context_with_limit(mcp, conversation_messages):
    """Test getting limited context from a session."""
    session_id = "test_session"
    for msg in conversation_messages:
        mcp.add_message(session_id, msg.role, msg.content)

    limit = 3
    context = mcp.get_context(session_id, max_messages=limit)

    assert len(context) == limit
    # Should return the most recent messages
    for original, retrieved in zip(conversation_messages[-limit:], context):
        assert retrieved.role == original.role
        assert retrieved.content == original.content

def test_multiple_sessions(mcp):
    """Test handling multiple independent sessions."""
    sessions = {
        "user1": [("user", "Message 1"), ("assistant", "Response 1")],
        "user2": [("user", "Different message"), ("assistant", "Different response")],
        "user3": [("user", "Another conversation")]
    }

    for session_id, messages in sessions.items():
        for role, content in messages:
            mcp.add_message(session_id, role, content)

    assert len(mcp.conversations) == len(sessions)
    for session_id, messages in sessions.items():
        context = mcp.get_context(session_id)
        assert len(context) == len(messages)
        for i, (role, content) in enumerate(messages):
            assert context[i].role == role
            assert context[i].content == content

def test_empty_message_handling(mcp):
    """Test handling empty or whitespace-only messages."""
    session_id = "test_session"

    mcp.add_message(session_id, "user", "")
    mcp.add_message(session_id, "assistant", "   ")

    context = mcp.get_context(session_id)
    assert len(context) == 2
    assert context[0].content == ""
    assert context[1].content == "   "

def test_long_conversation_history(mcp):
    """Test handling long conversation histories."""
    session_id = "test_session"
    num_messages = 100

    # Add many messages
    for i in range(num_messages):
        role = "user" if i % 2 == 0 else "assistant"
        mcp.add_message(session_id, role, f"Message {i}")

    # Test with different context sizes
    full_context = mcp.get_context(session_id)
    assert len(full_context) <= num_messages

    # Test with custom limit
    custom_limit = 5
    limited_context = mcp.get_context(session_id, max_messages=custom_limit)
    assert len(limited_context) == custom_limit
    assert limited_context[0].content == f"Message {num_messages-custom_limit}"

def test_role_validation(mcp):
    """Test message role validation."""
    session_id = "test_session"
    valid_roles = ["user", "assistant", "system"]

    # Test valid roles
    for role in valid_roles:
        mcp.add_message(session_id, role, "Test message")
        messages = mcp.conversations[session_id].messages
        assert messages[-1].role == role

    # Test custom role handling
    custom_role = "custom_assistant"
    mcp.add_message(session_id, custom_role, "Test message")
    messages = mcp.conversations[session_id].messages
    assert messages[-1].role == custom_role

def test_conversation_access(mcp):
    """Test conversation message access behavior."""
    session_id = "test_session"
    mcp.create_session(session_id)

    # Add some messages
    mcp.add_message(session_id, "user", "Message 1")
    mcp.add_message(session_id, "assistant", "Response 1")

    # Get messages snapshot
    messages = mcp.get_context(session_id)

    # Verify message access
    assert len(messages) == 2
    assert messages[0].role == "user"
    assert messages[0].content == "Message 1"
    assert messages[1].role == "assistant"
    assert messages[1].content == "Response 1"

    # Add new message and verify original snapshot unchanged
    mcp.add_message(session_id, "user", "Message 2")
    assert len(messages) == 2  # Original snapshot should be unchanged

def test_concurrent_sessions(mcp):
    """Test handling messages for multiple sessions concurrently."""
    sessions = ["user1", "user2", "user3"]
    messages_per_session = 50
    default_limit = 10  # MCP's default context size limit

    # Interleave messages between sessions
    for i in range(messages_per_session):
        for session_id in sessions:
            mcp.add_message(session_id, "user", f"Message {i} for {session_id}")
            mcp.add_message(session_id, "assistant", f"Response {i} for {session_id}")

    # Verify each session maintained its own context correctly
    for session_id in sessions:
        context = mcp.get_context(session_id)
        assert len(context) == default_limit  # Should respect default limit
        # Check that messages are from the correct session
        assert all(msg.content.endswith(f"for {session_id}") for msg in context)
        # Verify we have the most recent messages
        start_idx = messages_per_session - (default_limit // 2)
        for i, msg in enumerate(context[::2]):  # Check user messages
            assert msg.content == f"Message {start_idx + i} for {session_id}"
