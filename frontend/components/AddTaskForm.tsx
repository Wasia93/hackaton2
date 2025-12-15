/**
 * Add task form component
 * Task: T-027 - Create Add Task Form Component
 */

"use client"

import { useState, FormEvent } from "react"
import { CreateTaskRequest } from "@/types/task"

interface AddTaskFormProps {
  onCreate: (data: CreateTaskRequest) => Promise<void>
}

export default function AddTaskForm({ onCreate }: AddTaskFormProps) {
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [error, setError] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError("")

    // Validation
    if (!title.trim()) {
      setError("Title is required")
      return
    }

    if (title.length > 200) {
      setError("Title must be 200 characters or less")
      return
    }

    setIsSubmitting(true)

    try {
      await onCreate({ title: title.trim(), description: description.trim() })
      // Clear form on success
      setTitle("")
      setDescription("")
    } catch (err: any) {
      setError(err.message || "Failed to create task")
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white p-6 rounded-lg shadow mb-6"
    >
      <h2 className="text-xl font-bold mb-4">Add New Task</h2>

      {error && (
        <div className="bg-red-100 text-red-700 p-3 rounded mb-4" role="alert">
          {error}
        </div>
      )}

      <div className="mb-4">
        <label htmlFor="task-title" className="block mb-2 font-semibold">
          Title <span className="text-red-500">*</span>
        </label>
        <input
          id="task-title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Enter task title..."
          maxLength={200}
          disabled={isSubmitting}
          required
        />
        <p className="text-xs text-gray-500 mt-1">
          {title.length}/200 characters
        </p>
      </div>

      <div className="mb-4">
        <label htmlFor="task-description" className="block mb-2 font-semibold">
          Description
        </label>
        <textarea
          id="task-description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          rows={3}
          placeholder="Enter task description (optional)..."
          disabled={isSubmitting}
        />
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
      >
        {isSubmitting ? "Adding..." : "Add Task"}
      </button>
    </form>
  )
}
