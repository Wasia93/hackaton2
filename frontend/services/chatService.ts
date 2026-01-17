/**
 * Chat API service
 * Task: T-028 - Integrate chat API client
 */

import { apiRequest } from "@/lib/api"

// Types for chat API
export interface ChatRequest {
  message: string
  conversation_id?: number
}

export interface ToolCallInfo {
  name: string
  arguments: Record<string, any>
  result: Record<string, any>
}

export interface ChatResponse {
  conversation_id: number
  message_id: number
  content: string
  tool_calls?: ToolCallInfo[]
}

export interface Conversation {
  id: number
  title: string
  created_at: string
  updated_at: string
  message_count?: number
}

export interface Message {
  id: number
  role: "user" | "assistant"
  content: string
  tool_calls?: any
  created_at: string
}

export interface ConversationsListResponse {
  conversations: Conversation[]
  total: number
}

export interface ConversationMessagesResponse {
  conversation_id: number
  title: string
  messages: Message[]
  total: number
}

export const chatService = {
  /**
   * Send a message to the AI assistant
   */
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    return apiRequest<ChatResponse>("/api/chat", {
      method: "POST",
      body: JSON.stringify(request),
    })
  },

  /**
   * Get all conversations for the current user
   */
  async getConversations(): Promise<ConversationsListResponse> {
    return apiRequest<ConversationsListResponse>("/api/conversations")
  },

  /**
   * Get messages for a specific conversation
   */
  async getConversationMessages(conversationId: number): Promise<ConversationMessagesResponse> {
    return apiRequest<ConversationMessagesResponse>(`/api/conversations/${conversationId}`)
  },

  /**
   * Delete a conversation
   */
  async deleteConversation(conversationId: number): Promise<void> {
    return apiRequest<void>(`/api/conversations/${conversationId}`, {
      method: "DELETE",
    })
  },

  /**
   * Check if chat service is healthy
   */
  async checkHealth(): Promise<{ status: string; openai_configured: boolean; model: string }> {
    return apiRequest<{ status: string; openai_configured: boolean; model: string }>("/api/chat/health")
  },
}
