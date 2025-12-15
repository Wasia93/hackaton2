/**
 * Dashboard page with task management - Refactored with components
 * Task: T-030 - Create Dashboard Page (updated with T-026-T-028, T-032, T-033)
 */

"use client"

import { useState, useEffect } from "react"
import { Task, CreateTaskRequest, UpdateTaskRequest } from "@/types/task"
import { taskService } from "@/services/taskService"
import AddTaskForm from "@/components/AddTaskForm"
import TaskList from "@/components/TaskList"
import EditTaskModal from "@/components/EditTaskModal"
import TaskStats from "@/components/TaskStats"

type FilterType = "all" | "completed" | "incomplete"
type SortType = "date" | "title"

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState("")

  // Edit modal state
  const [editingTask, setEditingTask] = useState<Task | null>(null)

  // Filter and sort state (T-032)
  const [filter, setFilter] = useState<FilterType>("all")
  const [sortBy, setSortBy] = useState<SortType>("date")

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

  const handleCreate = async (data: CreateTaskRequest) => {
    const newTask = await taskService.createTask(data)
    setTasks([...tasks, newTask])
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

  const handleUpdate = async (id: number, data: UpdateTaskRequest) => {
    const updatedTask = await taskService.updateTask(id, data)
    setTasks(tasks.map((t) => (t.id === id ? updatedTask : t)))
  }

  // Filter and sort tasks (T-032)
  const filteredAndSortedTasks = tasks
    .filter((task) => {
      if (filter === "completed") return task.completed
      if (filter === "incomplete") return !task.completed
      return true
    })
    .sort((a, b) => {
      if (sortBy === "title") {
        return a.title.localeCompare(b.title)
      }
      // Sort by date (newest first)
      return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading tasks...</p>
        </div>
      </div>
    )
  }

  return (
    <div>
      {/* Task Statistics (T-033) */}
      <TaskStats tasks={tasks} />

      {/* Add Task Form (T-027) */}
      <AddTaskForm onCreate={handleCreate} />

      {/* Error Display */}
      {error && (
        <div className="bg-red-100 text-red-700 p-4 rounded mb-4" role="alert">
          {error}
        </div>
      )}

      {/* Filter and Sort Controls (T-032) */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <label htmlFor="filter" className="block text-sm font-semibold mb-2">
              Filter Tasks
            </label>
            <select
              id="filter"
              value={filter}
              onChange={(e) => setFilter(e.target.value as FilterType)}
              className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Tasks</option>
              <option value="completed">Completed Only</option>
              <option value="incomplete">Incomplete Only</option>
            </select>
          </div>

          <div className="flex-1">
            <label htmlFor="sort" className="block text-sm font-semibold mb-2">
              Sort By
            </label>
            <select
              id="sort"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as SortType)}
              className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-blue-500"
            >
              <option value="date">Date (Newest First)</option>
              <option value="title">Title (A-Z)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Task List (T-026) */}
      <TaskList
        tasks={filteredAndSortedTasks}
        onToggle={handleToggle}
        onEdit={setEditingTask}
        onDelete={handleDelete}
      />

      {/* Edit Modal (T-028) */}
      <EditTaskModal
        task={editingTask}
        onUpdate={handleUpdate}
        onClose={() => setEditingTask(null)}
      />
    </div>
  )
}
