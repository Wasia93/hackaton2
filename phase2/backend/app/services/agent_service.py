"""
Agent Service Layer
Task: T-017, T-018 - Integrate MCP tools with agent and create service layer

This service handles communication between the chat API and the AI agent,
processing messages and executing tool calls.

Uses OpenAI API with gpt-4o-mini for fast responses.
"""

import json
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from app.core.config import settings
from app.mcp_server import mcp_server
from app.services.agent_config import (
    AGENT_INSTRUCTIONS,
    AGENT_TEMPERATURE,
)


class AgentService:
    """
    Service for processing chat messages through the OpenAI agent.
    Handles tool execution and response generation.
    """

    def __init__(self):
        """Initialize the agent service with OpenAI client."""
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model_name = "gpt-4o-mini"
        self.tools = mcp_server.get_tools()

    async def process_message(
        self,
        user_id: str,
        message_content: str,
        conversation_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Process a user message through the OpenAI agent.

        Args:
            user_id: The authenticated user's ID
            message_content: The user's message content
            conversation_history: Previous messages in the conversation

        Returns:
            Dictionary with:
                - content: The agent's response text
                - tool_calls: List of tools that were called (if any)
        """
        # Build messages
        messages = [{"role": "system", "content": AGENT_INSTRUCTIONS}]

        if conversation_history:
            for msg in conversation_history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        messages.append({"role": "user", "content": message_content})

        # Call OpenAI
        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            tools=self.tools if self.tools else None,
            temperature=AGENT_TEMPERATURE,
        )

        tool_calls_made = []
        choice = response.choices[0]

        # Handle tool calls
        if choice.finish_reason == "tool_calls" and choice.message.tool_calls:
            # Add assistant message with tool calls as dict
            assistant_msg = {
                "role": "assistant",
                "content": choice.message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        }
                    }
                    for tc in choice.message.tool_calls
                ]
            }
            messages.append(assistant_msg)

            for tc in choice.message.tool_calls:
                tool_name = tc.function.name
                tool_args = json.loads(tc.function.arguments)

                # Inject user_id
                tool_args["user_id"] = user_id

                # Execute the tool
                result = await mcp_server.execute_tool(tool_name, tool_args)

                tool_calls_made.append({
                    "id": tc.id,
                    "name": tool_name,
                    "arguments": tool_args,
                    "result": result
                })

                # Add tool result
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps(result)
                })

            # Get final response after tool execution
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=AGENT_TEMPERATURE,
            )
            choice = response.choices[0]

        response_text = choice.message.content or ""

        return {
            "content": response_text or "I apologize, I couldn't generate a response.",
            "tool_calls": tool_calls_made if tool_calls_made else None
        }


# Global agent service instance
agent_service = AgentService()


async def process_chat_message(
    user_id: str,
    message_content: str,
    conversation_history: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Convenience function to process a chat message.

    Args:
        user_id: The authenticated user's ID
        message_content: The user's message content
        conversation_history: Previous messages in the conversation

    Returns:
        Dictionary with content and tool_calls
    """
    return await agent_service.process_message(
        user_id, message_content, conversation_history
    )
