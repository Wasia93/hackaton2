"""
Kafka Event Consumer for task analytics
Phase V: Cloud Deployment - Event Streaming

Can run as:
  - Standalone worker: python -m app.services.event_consumer
  - Part of backend with /analytics endpoint
"""

import json
import os
import asyncio
import logging
import signal
from datetime import datetime
from collections import defaultdict
from typing import Optional, Any

logger = logging.getLogger(__name__)


class EventConsumer:
    """
    Consumes task events from Kafka and tracks analytics.
    """

    _instance: Optional['EventConsumer'] = None
    _consumer: Any = None
    _running: bool = False

    def __init__(self):
        self.bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.enabled = os.getenv('KAFKA_ENABLED', 'false').lower() == 'true'
        self.topic = os.getenv('KAFKA_TOPIC', 'task-events')
        self.group_id = os.getenv('KAFKA_CONSUMER_GROUP', 'todo-analytics')

        # Analytics data
        self.total_events = 0
        self.events_by_type: dict[str, int] = defaultdict(int)
        self.events_by_user: dict[str, int] = defaultdict(int)
        self.recent_events: list[dict] = []
        self.started_at: Optional[str] = None

    @classmethod
    async def get_instance(cls) -> 'EventConsumer':
        """Get singleton instance."""
        if cls._instance is None:
            cls._instance = EventConsumer()
        return cls._instance

    async def start(self):
        """Start consuming events from Kafka."""
        if not self.enabled:
            logger.info("Kafka consumer disabled (KAFKA_ENABLED=false)")
            return

        try:
            from aiokafka import AIOKafkaConsumer

            self._consumer = AIOKafkaConsumer(
                self.topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                auto_offset_reset='earliest',
                enable_auto_commit=True,
            )
            await self._consumer.start()
            self._running = True
            self.started_at = datetime.utcnow().isoformat() + "Z"
            logger.info(f"Event consumer started, listening on topic: {self.topic}")

            asyncio.create_task(self._consume_loop())
        except ImportError:
            logger.warning("aiokafka not installed, event consumer disabled")
            self.enabled = False
        except Exception as e:
            logger.error(f"Failed to start event consumer: {e}")
            self.enabled = False

    async def _consume_loop(self):
        """Main consumption loop."""
        try:
            async for msg in self._consumer:
                if not self._running:
                    break
                await self._process_event(msg.value)
        except Exception as e:
            if self._running:
                logger.error(f"Consumer loop error: {e}")

    async def _process_event(self, event: dict):
        """Process a single event and update analytics."""
        self.total_events += 1

        event_type = event.get("event_type", "unknown")
        user_id = event.get("user_id", "unknown")

        self.events_by_type[event_type] += 1
        self.events_by_user[user_id] += 1

        # Keep last 100 events
        self.recent_events.append({
            "event_id": event.get("event_id"),
            "event_type": event_type,
            "timestamp": event.get("timestamp"),
            "user_id": user_id,
            "task_id": event.get("payload", {}).get("task_id"),
        })
        if len(self.recent_events) > 100:
            self.recent_events = self.recent_events[-100:]

        logger.debug(f"Processed event: {event_type} (total: {self.total_events})")

    def get_analytics(self) -> dict:
        """Get current analytics data."""
        return {
            "status": "running" if self._running else "stopped",
            "enabled": self.enabled,
            "started_at": self.started_at,
            "total_events": self.total_events,
            "events_by_type": dict(self.events_by_type),
            "unique_users": len(self.events_by_user),
            "recent_events_count": len(self.recent_events),
            "recent_events": self.recent_events[-10:],
        }

    async def stop(self):
        """Stop the consumer."""
        self._running = False
        if self._consumer:
            await self._consumer.stop()
            logger.info("Event consumer stopped")


async def main():
    """Run the event consumer as a standalone worker."""
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting standalone event consumer...")

    consumer = EventConsumer()
    consumer.enabled = True

    loop = asyncio.get_event_loop()
    stop_event = asyncio.Event()

    def shutdown():
        logger.info("Shutdown signal received")
        stop_event.set()

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, shutdown)
        except NotImplementedError:
            signal.signal(sig, lambda s, f: shutdown())

    await consumer.start()

    if consumer._running:
        logger.info("Consumer is running. Press Ctrl+C to stop.")
        await stop_event.wait()
        await consumer.stop()
    else:
        logger.error("Consumer failed to start. Check KAFKA_BOOTSTRAP_SERVERS.")


if __name__ == "__main__":
    asyncio.run(main())
