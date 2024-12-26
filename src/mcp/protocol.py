from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class Message:
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class Conversation:
    messages: List[Message] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)

class ModelContextProtocol:
    def __init__(self):
        self.conversations: Dict[str, Conversation] = {}

    def create_session(self, session_id: str) -> None:
        if session_id not in self.conversations:
            self.conversations[session_id] = Conversation()

    def add_message(self, session_id: str, role: str, content: str) -> None:
        self.create_session(session_id)
        self.conversations[session_id].messages.append(
            Message(role=role, content=content)
        )

    def get_context(self, session_id: str, max_messages: int = 10) -> List[Message]:
        if session_id not in self.conversations:
            return []
        return self.conversations[session_id].messages[-max_messages:]

    def clear_session(self, session_id: str) -> None:
        if session_id in self.conversations:
            del self.conversations[session_id]

    def update_metadata(self, session_id: str, metadata: Dict) -> None:
        self.create_session(session_id)
        self.conversations[session_id].metadata.update(metadata)

    def get_metadata(self, session_id: str) -> Dict:
        if session_id not in self.conversations:
            return {}
        return self.conversations[session_id].metadata
