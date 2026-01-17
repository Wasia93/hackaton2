"""
Conversation Service Layer
Task: T-020 - Create conversation service

Handles conversation CRUD operations and history loading.
"""

from sqlmodel import Session, select
from app.models.conversation import Conversation
from app.models.message import Message
from typing import Optional, List
from datetime import datetime


class ConversationService:
    """
    Service layer for conversation-related business logic.
    Ensures data isolation by filtering all queries by user_id.
    """

    def __init__(self, session: Session, user_id: str):
        """
        Initialize conversation service.

        Args:
            session: Database session
            user_id: Current user's ID (from JWT token)
        """
        self.session = session
        self.user_id = user_id

    def create_conversation(self, title: str = "New Conversation") -> Conversation:
        """
        Create a new conversation for the current user.

        Args:
            title: Conversation title (default: "New Conversation")

        Returns:
            Conversation: Created conversation object
        """
        conversation = Conversation(
            user_id=self.user_id,
            title=title[:200]  # Ensure max length
        )

        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)

        return conversation

    def get_conversation_by_id(self, conversation_id: int) -> Optional[Conversation]:
        """
        Get a specific conversation by ID (only if owned by current user).

        Args:
            conversation_id: Conversation ID to retrieve

        Returns:
            Optional[Conversation]: Conversation if found and owned by user, None otherwise
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == self.user_id
        )
        return self.session.exec(statement).first()

    def get_all_conversations(self) -> List[Conversation]:
        """
        Get all conversations for the current user, ordered by most recent.

        Returns:
            List[Conversation]: List of conversations owned by current user
        """
        statement = select(Conversation).where(
            Conversation.user_id == self.user_id
        ).order_by(Conversation.updated_at.desc())
        return list(self.session.exec(statement).all())

    def update_conversation_title(
        self,
        conversation_id: int,
        title: str
    ) -> Optional[Conversation]:
        """
        Update a conversation's title.

        Args:
            conversation_id: Conversation ID to update
            title: New title

        Returns:
            Optional[Conversation]: Updated conversation if found, None otherwise
        """
        conversation = self.get_conversation_by_id(conversation_id)
        if not conversation:
            return None

        conversation.title = title[:200]
        conversation.updated_at = datetime.utcnow()

        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)

        return conversation

    def update_conversation_timestamp(self, conversation_id: int) -> Optional[Conversation]:
        """
        Update a conversation's updated_at timestamp.
        Called when a new message is added.

        Args:
            conversation_id: Conversation ID to update

        Returns:
            Optional[Conversation]: Updated conversation if found, None otherwise
        """
        conversation = self.get_conversation_by_id(conversation_id)
        if not conversation:
            return None

        conversation.updated_at = datetime.utcnow()

        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)

        return conversation

    def delete_conversation(self, conversation_id: int) -> bool:
        """
        Delete a conversation by ID (cascade deletes messages).

        Args:
            conversation_id: Conversation ID to delete

        Returns:
            bool: True if deleted, False if not found
        """
        conversation = self.get_conversation_by_id(conversation_id)
        if not conversation:
            return False

        # Delete associated messages first (if not using cascade)
        statement = select(Message).where(Message.conversation_id == conversation_id)
        messages = self.session.exec(statement).all()
        for message in messages:
            self.session.delete(message)

        self.session.delete(conversation)
        self.session.commit()

        return True

    def get_or_create_conversation(self, conversation_id: Optional[int] = None) -> Conversation:
        """
        Get an existing conversation or create a new one.

        Args:
            conversation_id: Optional conversation ID to retrieve

        Returns:
            Conversation: Existing or newly created conversation
        """
        if conversation_id:
            conversation = self.get_conversation_by_id(conversation_id)
            if conversation:
                return conversation

        # Create new conversation if not found or not provided
        return self.create_conversation()
