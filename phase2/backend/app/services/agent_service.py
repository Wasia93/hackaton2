"""
Agent Service Layer
Task: T-017, T-018 - Integrate MCP tools with agent and create service layer

This service handles communication between the chat API and the AI agent,
processing messages and executing tool calls.

Updated to use Google Gemini API.
"""

import json
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from app.core.config import settings
from app.mcp_server import mcp_server
from app.services.agent_config import (
    AGENT_INSTRUCTIONS,
    AGENT_TEMPERATURE,
)


class AgentService:
    """
    Service for processing chat messages through the Gemini agent.
    Handles tool execution and response generation.
    """

    def __init__(self):
        """Initialize the agent service with Gemini client."""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model_name = settings.GEMINI_MODEL or "gemini-1.5-flash"
        self.tools = mcp_server.get_tools()

        # Convert OpenAI tool format to Gemini function declarations
        self.gemini_tools = self._convert_tools_to_gemini_format()

    def _convert_tools_to_gemini_format(self) -> List[Dict]:
        """Convert OpenAI-style tools to Gemini function declarations."""
        function_declarations = []
        for tool in self.tools:
            func = tool.get("function", {})
            params = func.get("parameters", {})

            # Convert parameters to Gemini format
            properties = {}
            required = params.get("required", [])

            for prop_name, prop_def in params.get("properties", {}).items():
                prop_type = prop_def.get("type", "string")
                # Map types
                type_mapping = {
                    "string": "STRING",
                    "integer": "INTEGER",
                    "number": "NUMBER",
                    "boolean": "BOOLEAN",
                }
                properties[prop_name] = {
                    "type": type_mapping.get(prop_type, "STRING"),
                    "description": prop_def.get("description", ""),
                }

            function_declarations.append({
                "name": func.get("name"),
                "description": func.get("description"),
                "parameters": {
                    "type": "OBJECT",
                    "properties": properties,
                    "required": required,
                }
            })

        return function_declarations

    async def process_message(
        self,
        user_id: str,
        message_content: str,
        conversation_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Process a user message through the Gemini agent.

        Args:
            user_id: The authenticated user's ID
            message_content: The user's message content
            conversation_history: Previous messages in the conversation

        Returns:
            Dictionary with:
                - content: The agent's response text
                - tool_calls: List of tools that were called (if any)
        """
        # Create model with tools
        model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=AGENT_INSTRUCTIONS,
            tools=[{"function_declarations": self.gemini_tools}],
        )

        # Build conversation history for Gemini
        history = []
        if conversation_history:
            for msg in conversation_history:
                role = "user" if msg["role"] == "user" else "model"
                history.append({
                    "role": role,
                    "parts": [msg["content"]]
                })

        # Start chat
        chat = model.start_chat(history=history)

        # Send message
        response = chat.send_message(message_content)

        tool_calls_made = []

        # Check for function calls
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    fc = part.function_call
                    tool_name = fc.name
                    tool_args = dict(fc.args)

                    # Inject user_id
                    tool_args["user_id"] = user_id

                    # Execute the tool
                    result = await mcp_server.execute_tool(tool_name, tool_args)

                    tool_calls_made.append({
                        "id": f"call_{tool_name}",
                        "name": tool_name,
                        "arguments": tool_args,
                        "result": result
                    })

                    # Send function response back to get final answer
                    response = chat.send_message(
                        genai.protos.Content(
                            parts=[genai.protos.Part(
                                function_response=genai.protos.FunctionResponse(
                                    name=tool_name,
                                    response={"result": result}
                                )
                            )]
                        )
                    )

        # Extract text response
        response_text = ""
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'text') and part.text:
                    response_text += part.text

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
