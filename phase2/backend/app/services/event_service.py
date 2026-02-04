"""
Kafka Event Service for publishing task events
Phase V: Cloud Deployment - Event Streaming
"""

import json
import os
from datetime import datetime
from uuid import uuid4
from typing import Optional, Any
import logging

logger = logging.getLogger(__name__)


class EventService:
    """
    Service for publishing task events to Kafka/Redpanda.
    Supports async event publishing with graceful degradation.
    """

    _instance: Optional['EventService'] = None
    _producer: Any = None
    _initialized: bool = False

    def __init__(self):
        self.bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.enabled = os.getenv('KAFKA_ENABLED', 'false').lower() == 'true'
        self.topic = os.getenv('KAFKA_TOPIC', 'task-events')

    @classmethod
    async def get_instance(cls) -> 'EventService':
        """Get singleton instance of EventService."""
        if cls._instance is None:
            cls._instance = EventService()
            if cls._instance.enabled:
                await cls._instance._connect()
        return cls._instance

    async def _connect(self):
        """Connect to Kafka broker."""
        if self._initialized:
            return

        try:
            from aiokafka import AIOKafkaProducer

            self._producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                acks='all',  # Wait for all replicas
                retries=3,
                retry_backoff_ms=500
            )
            await self._producer.start()
            self._initialized = True
            logger.info(f"Connected to Kafka at {self.bootstrap_servers}")
        except ImportError:
            logger.warning("aiokafka not installed, event publishing disabled")
            self.enabled = False
        except Exception as e:
            logger.error(f"Failed to connect to Kafka: {e}")
            self.enabled = False

    async def publish_task_event(
        self,
        event_type: str,
        task_id: int,
        user_id: str,
        payload: dict
    ) -> bool:
        """
        Publish a task event to Kafka.

        Args:
            event_type: Type of event (task.created, task.updated, etc.)
            task_id: ID of the task
            user_id: ID of the user who performed the action
            payload: Additional event data

        Returns:
            bool: True if published successfully, False otherwise
        """
        if not self.enabled or not self._producer:
            return False

        event = {
            "event_id": str(uuid4()),
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "user_id": user_id,
            "payload": {
                "task_id": task_id,
                **payload
            }
        }

        try:
            await self._producer.send_and_wait(self.topic, event)
            logger.debug(f"Published event: {event_type} for task {task_id}")
            return True
        except Exception as e:
            # Log error but don't fail the request
            logger.error(f"Failed to publish event {event_type}: {e}")
            return False

    async def publish_task_created(self, task_id: int, user_id: str, title: str, description: str = ""):
        """Publish task created event."""
        return await self.publish_task_event(
            "task.created",
            task_id,
            user_id,
            {"title": title, "description": description, "completed": False}
        )

    async def publish_task_updated(self, task_id: int, user_id: str, title: str = None, description: str = None):
        """Publish task updated event."""
        payload = {}
        if title is not None:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        return await self.publish_task_event("task.updated", task_id, user_id, payload)

    async def publish_task_completed(self, task_id: int, user_id: str, completed: bool):
        """Publish task completion toggled event."""
        return await self.publish_task_event(
            "task.completed" if completed else "task.uncompleted",
            task_id,
            user_id,
            {"completed": completed}
        )

    async def publish_task_deleted(self, task_id: int, user_id: str):
        """Publish task deleted event."""
        return await self.publish_task_event("task.deleted", task_id, user_id, {})

    async def close(self):
        """Close the Kafka producer connection."""
        if self._producer:
            await self._producer.stop()
            self._initialized = False
            logger.info("Kafka producer closed")


# Synchronous wrapper for non-async contexts
def get_event_service_sync() -> EventService:
    """Get event service instance (creates new if needed)."""
    if EventService._instance is None:
        EventService._instance = EventService()
    return EventService._instance
