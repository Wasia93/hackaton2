/**
 * Edit task modal component
 * Task: T-028 - Create Edit Task Modal Component
 */

"use client"

import { useState, useEffect, FormEvent } from "react"
import { Task, UpdateTaskRequest } from "@/types/task"

interface EditTaskModalProps {
  task: Task | null
  onUpdate: (id: number, data: UpdateTaskRequest) => Promise<void>
  onClose: () => void
}

export default function EditTaskModal({
  task,
  onUpdate,
  onClose,
}: EditTaskModalProps) {
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [error, setError] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Update form when task changes
  useEffect(() => {
    if (task) {
      setTitle(task.title)
      setDescription(task.description)
      setError("")
    }
  }, [task])

  // Don't render if no task selected
  if (!task) return null

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
      await onUpdate(task.id, {
        title: title.trim(),
        description: description.trim(),
      })
      onClose()
    } catch (err: any) {
      setError(err.message || "Failed to update task")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleBackdropClick = (e: React.MouseEvent) => {
    // Close modal if clicking backdrop (not the modal content)
    if (e.target === e.currentTarget) {
      onClose()
    }
  }

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      onClick={handleBackdropClick}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <div className="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
        <h2 id="modal-title" className="text-xl font-bold mb-4">
          Edit Task
        </h2>

        {error && (
          <div className="bg-red-100 text-red-700 p-3 rounded mb-4" role="alert">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="edit-title" className="block mb-2 font-semibold">
              Title <span className="text-red-500">*</span>
            </label>
            <input
              id="edit-title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              maxLength={200}
              disabled={isSubmitting}
              required
            />
            <p className="text-xs text-gray-500 mt-1">
              {title.length}/200 characters
            </p>
          </div>

          <div className="mb-4">
            <label
              htmlFor="edit-description"
              className="block mb-2 font-semibold"
            >
              Description
            </label>
            <textarea
              id="edit-description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows={3}
              disabled={isSubmitting}
            />
          </div>

          <div className="flex gap-4">
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex-1 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
            >
              {isSubmitting ? "Saving..." : "Save Changes"}
            </button>
            <button
              type="button"
              onClick={onClose}
              disabled={isSubmitting}
              className="flex-1 bg-gray-300 px-4 py-2 rounded hover:bg-gray-400 disabled:bg-gray-200 disabled:cursor-not-allowed transition"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
