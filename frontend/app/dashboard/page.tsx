/**
 * Dashboard page with task management
 * Task: T-030 - Create Dashboard Page
 */

"use client"

import { useState, useEffect } from "react"
import { Task, CreateTaskRequest, UpdateTaskRequest } from "@/types/task"
import { taskService } from "@/services/taskService"

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState("")

  // Add task form state
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [isAdding, setIsAdding] = useState(false)

  // Edit modal state
  const [editingTask, setEditingTask] = useState<Task | null>(null)
  const [editTitle, setEditTitle] = useState("")
  const [editDescription, setEditDescription] = useState("")

  useEffect(() => {
    fetchTasks()
  }, [])

  const fetchTasks = async () => {
    try {
      setIsLoading(true)
      const data = await taskService.getAllTasks()
      setTasks(data)
    } catch (err: any) {
      setError(err.message || "Failed to load tasks")
    } finally {
      setIsLoading(false)
    }
  }

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!title.trim()) return

    try {
      setIsAdding(true)
      const newTask = await taskService.createTask({ title, description })
      setTasks([...tasks, newTask])
      setTitle("")
      setDescription("")
    } catch (err: any) {
      alert("Failed to create task: " + err.message)
    } finally {
      setIsAdding(false)
    }
  }

  const handleToggle = async (id: number) => {
    try {
      const updatedTask = await taskService.toggleCompletion(id)
      setTasks(tasks.map((t) => (t.id === id ? updatedTask : t)))
    } catch (err: any) {
      alert("Failed to toggle task: " + err.message)
    }
  }

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this task?")) return

    try {
      await taskService.deleteTask(id)
      setTasks(tasks.filter((t) => t.id !== id))
    } catch (err: any) {
      alert("Failed to delete task: " + err.message)
    }
  }

  const openEditModal = (task: Task) => {
    setEditingTask(task)
    setEditTitle(task.title)
    setEditDescription(task.description)
  }

  const closeEditModal = () => {
    setEditingTask(null)
    setEditTitle("")
    setEditDescription("")
  }

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!editingTask) return

    try {
      const updatedTask = await taskService.updateTask(editingTask.id, {
        title: editTitle,
        description: editDescription,
      })
      setTasks(tasks.map((t) => (t.id === editingTask.id ? updatedTask : t)))
      closeEditModal()
    } catch (err: any) {
      alert("Failed to update task: " + err.message)
    }
  }

  if (isLoading) {
    return <div className="text-center py-8">Loading tasks...</div>
  }

  return (
    <div>
      {/* Add Task Form */}
      <form
        onSubmit={handleCreate}
        className="bg-white p-6 rounded-lg shadow mb-6"
      >
        <h2 className="text-xl font-bold mb-4">Add New Task</h2>

        <div className="mb-4">
          <label className="block mb-2 font-semibold">Title *</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full border p-2 rounded"
            placeholder="Enter task title..."
            maxLength={200}
            disabled={isAdding}
            required
          />
        </div>

        <div className="mb-4">
          <label className="block mb-2 font-semibold">Description</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full border p-2 rounded"
            rows={3}
            placeholder="Enter task description (optional)..."
            disabled={isAdding}
          />
        </div>

        <button
          type="submit"
          disabled={isAdding}
          className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400 transition"
        >
          {isAdding ? "Adding..." : "Add Task"}
        </button>
      </form>

      {/* Error Display */}
      {error && (
        <div className="bg-red-100 text-red-700 p-4 rounded mb-4">{error}</div>
      )}

      {/* Task List */}
      <div className="space-y-4">
        {tasks.length === 0 ? (
          <div className="text-center text-gray-500 py-8 bg-white rounded-lg">
            No tasks yet. Create your first task above!
          </div>
        ) : (
          tasks.map((task) => (
            <div
              key={task.id}
              className="bg-white p-4 rounded-lg shadow flex items-start gap-4"
            >
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => handleToggle(task.id)}
                className="mt-1 w-5 h-5"
              />

              <div className="flex-1">
                <h3
                  className={`font-semibold text-lg ${
                    task.completed ? "line-through text-gray-500" : ""
                  }`}
                >
                  {task.title}
                </h3>
                {task.description && (
                  <p className="text-gray-600 text-sm mt-1">
                    {task.description}
                  </p>
                )}
                <p className="text-xs text-gray-400 mt-2">
                  {new Date(task.created_at).toLocaleString()}
                </p>
              </div>

              <div className="flex gap-2">
                <button
                  onClick={() => openEditModal(task)}
                  className="text-blue-500 hover:text-blue-700 px-3 py-1 border border-blue-500 rounded hover:bg-blue-50 transition"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(task.id)}
                  className="text-red-500 hover:text-red-700 px-3 py-1 border border-red-500 rounded hover:bg-red-50 transition"
                >
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Edit Modal */}
      {editingTask && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg max-w-md w-full mx-4">
            <h2 className="text-xl font-bold mb-4">Edit Task</h2>

            <form onSubmit={handleUpdate}>
              <div className="mb-4">
                <label className="block mb-2 font-semibold">Title *</label>
                <input
                  type="text"
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  className="w-full border p-2 rounded"
                  maxLength={200}
                  required
                />
              </div>

              <div className="mb-4">
                <label className="block mb-2 font-semibold">Description</label>
                <textarea
                  value={editDescription}
                  onChange={(e) => setEditDescription(e.target.value)}
                  className="w-full border p-2 rounded"
                  rows={3}
                />
              </div>

              <div className="flex gap-4">
                <button
                  type="submit"
                  className="flex-1 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
                >
                  Save Changes
                </button>
                <button
                  type="button"
                  onClick={closeEditModal}
                  className="flex-1 bg-gray-300 px-4 py-2 rounded hover:bg-gray-400 transition"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
