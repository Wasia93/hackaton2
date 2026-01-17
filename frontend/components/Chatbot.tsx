/**
 * Chatbot Component
 * Task: T-027, T-029 - Create Chatbot component and add to dashboard
 *
 * A floating chatbot interface that allows users to manage tasks
 * through natural language conversation with the AI assistant.
 */

"use client"

import { useState, useRef, useEffect } from "react"
import { chatService, Message, ChatResponse } from "@/services/chatService"

interface ChatbotProps {
  onTasksChanged?: () => void // Callback to refresh tasks after chatbot makes changes
}

export default function Chatbot({ onTasksChanged }: ChatbotProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")
  const [conversationId, setConversationId] = useState<number | undefined>()

  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  // Focus input when chat opens
  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus()
    }
  }, [isOpen])

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return

    const userMessage = inputValue.trim()
    setInputValue("")
    setError("")

    // Add user message to chat immediately
    const userMsg: Message = {
      id: Date.now(),
      role: "user",
      content: userMessage,
      created_at: new Date().toISOString(),
    }
    setMessages((prev) => [...prev, userMsg])
    setIsLoading(true)

    try {
      const response: ChatResponse = await chatService.sendMessage({
        message: userMessage,
        conversation_id: conversationId,
      })

      // Update conversation ID
      setConversationId(response.conversation_id)

      // Add assistant message
      const assistantMsg: Message = {
        id: response.message_id,
        role: "assistant",
        content: response.content,
        tool_calls: response.tool_calls,
        created_at: new Date().toISOString(),
      }
      setMessages((prev) => [...prev, assistantMsg])

      // If tools were called, refresh the task list
      if (response.tool_calls && response.tool_calls.length > 0 && onTasksChanged) {
        onTasksChanged()
      }
    } catch (err: any) {
      setError(err.message || "Failed to send message")
      // Remove the user message if it failed
      setMessages((prev) => prev.filter((m) => m.id !== userMsg.id))
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const handleNewConversation = () => {
    setMessages([])
    setConversationId(undefined)
    setError("")
  }

  const formatToolCalls = (toolCalls: any[]) => {
    if (!toolCalls || toolCalls.length === 0) return null

    return (
      <div className="mt-2 text-xs text-gray-500 border-t border-gray-200 pt-2">
        <span className="font-medium">Actions performed:</span>
        <ul className="list-disc list-inside ml-2">
          {toolCalls.map((tc, i) => (
            <li key={i}>
              {tc.name.replace(/_/g, " ")}
              {tc.result?.success ? " ✓" : tc.result?.error ? ` (${tc.result.error})` : ""}
            </li>
          ))}
        </ul>
      </div>
    )
  }

  return (
    <>
      {/* Chat Toggle Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 w-14 h-14 bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-lg flex items-center justify-center transition-all z-50"
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        {isOpen ? (
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        ) : (
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
            />
          </svg>
        )}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 w-96 h-[500px] bg-white rounded-lg shadow-2xl flex flex-col z-50 border border-gray-200">
          {/* Header */}
          <div className="bg-blue-600 text-white p-4 rounded-t-lg flex items-center justify-between">
            <div>
              <h3 className="font-semibold">Task Assistant</h3>
              <p className="text-xs text-blue-100">Ask me to manage your tasks</p>
            </div>
            <button
              onClick={handleNewConversation}
              className="text-blue-100 hover:text-white text-sm"
              title="Start new conversation"
            >
              New Chat
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.length === 0 && (
              <div className="text-center text-gray-500 mt-8">
                <p className="mb-2">Hello! I can help you manage your tasks.</p>
                <p className="text-sm">Try saying:</p>
                <ul className="text-sm mt-2 space-y-1">
                  <li>&quot;Add buy groceries to my list&quot;</li>
                  <li>&quot;Show my tasks&quot;</li>
                  <li>&quot;Mark task 1 as done&quot;</li>
                </ul>
              </div>
            )}

            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[80%] p-3 rounded-lg ${
                    message.role === "user"
                      ? "bg-blue-600 text-white rounded-br-none"
                      : "bg-gray-100 text-gray-800 rounded-bl-none"
                  }`}
                >
                  <p className="whitespace-pre-wrap">{message.content}</p>
                  {message.role === "assistant" && message.tool_calls && formatToolCalls(message.tool_calls)}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 text-gray-800 p-3 rounded-lg rounded-bl-none">
                  <div className="flex items-center space-x-2">
                    <div className="animate-bounce w-2 h-2 bg-gray-400 rounded-full"></div>
                    <div className="animate-bounce w-2 h-2 bg-gray-400 rounded-full" style={{ animationDelay: "0.1s" }}></div>
                    <div className="animate-bounce w-2 h-2 bg-gray-400 rounded-full" style={{ animationDelay: "0.2s" }}></div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Error Display */}
          {error && (
            <div className="px-4 py-2 bg-red-100 text-red-700 text-sm">
              {error}
            </div>
          )}

          {/* Input */}
          <div className="p-4 border-t border-gray-200">
            <div className="flex space-x-2">
              <input
                ref={inputRef}
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type a message..."
                className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={isLoading}
              />
              <button
                onClick={handleSendMessage}
                disabled={isLoading || !inputValue.trim()}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
