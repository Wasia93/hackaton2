"""
Message Service Layer
Task: T-021 - Create message service

Handles message CRUD operations and conversation history retrieval.
"""

from sqlmodel import Session, select
from app.models.message import Message
from typing import Optional, List, Any, Dict
from datetime import datetime


class MessageService:
    """
    Service layer for message-related business logic.
    Messages are tied to conversations, which are owned by users.
    """

    def __init__(self, session: Session):
        """
        Initialize message service.

        Args:
            session: Database session
        """
        self.session = session

    def create_message(
        self,
        conversation_id: int,
        role: str,
        content: str,
        tool_calls: Optional[List[Dict[str, Any]]] = None
    ) -> Message:
        """
        Create a new message in a conversation.

        Args:
            conversation_id: ID of the conversation
            role: Message role ('user' or 'assistant')
            content: Message content
            tool_calls: Optional list of tool call details

        Returns:
            Message: Created message object
        """
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            tool_calls=tool_calls
        )

        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)

        return message

    def create_user_message(self, conversation_id: int, content: str) -> Message:
        """
        Create a user message in a conversation.

        Args:
            conversation_id: ID of the conversation
            content: Message content

        Returns:
            Message: Created user message
        """
        return self.create_message(
            conversation_id=conversation_id,
            role="user",
            content=content
        )

    def create_assistant_message(
        self,
        conversation_id: int,
        content: str,
        tool_calls: Optional[List[Dict[str, Any]]] = None
    ) -> Message:
        """
        Create an assistant message in a conversation.

        Args:
            conversation_id: ID of the conversation
            content: Message content
            tool_calls: Optional list of tool call details

        Returns:
            Message: Created assistant message
        """
        return self.create_message(
            conversation_id=conversation_id,
            role="assistant",
            content=content,
            tool_calls=tool_calls
        )

    def get_conversation_messages(
        self,
        conversation_id: int,
        limit: Optional[int] = None
    ) -> List[Message]:
        """
        Get all messages for a conversation, ordered by creation time.

        Args:
            conversation_id: ID of the conversation
            limit: Optional limit on number of messages to return

        Returns:
            List[Message]: List of messages in the conversation
        """
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc())

        if limit:
            statement = statement.limit(limit)

        return list(self.session.exec(statement).all())

    def get_conversation_history(
        self,
        conversation_id: int,
        max_messages: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get conversation history in OpenAI message format.

        Args:
            conversation_id: ID of the conversation
            max_messages: Maximum number of messages to return (default 50)

        Returns:
            List of message dictionaries in OpenAI format
        """
        messages = self.get_conversation_messages(conversation_id, limit=max_messages)

        return [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in messages
        ]

    def get_message_by_id(self, message_id: int) -> Optional[Message]:
        """
        Get a specific message by ID.

        Args:
            message_id: Message ID to retrieve

        Returns:
            Optional[Message]: Message if found, None otherwise
        """
        statement = select(Message).where(Message.id == message_id)
        return self.session.exec(statement).first()

    def delete_message(self, message_id: int) -> bool:
        """
        Delete a message by ID.

        Args:
            message_id: Message ID to delete

        Returns:
            bool: True if deleted, False if not found
        """
        message = self.get_message_by_id(message_id)
        if not message:
            return False

        self.session.delete(message)
        self.session.commit()

        return True

    def get_message_count(self, conversation_id: int) -> int:
        """
        Get the number of messages in a conversation.

        Args:
            conversation_id: ID of the conversation

        Returns:
            int: Number of messages
        """
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        )
        return len(list(self.session.exec(statement).all()))
