/**
 * Task API service
 * Task: T-029 - Create Task API Service
 */

import { apiRequest } from "@/lib/api"
import { Task, CreateTaskRequest, UpdateTaskRequest } from "@/types/task"

export const taskService = {
  /**
   * Get all tasks for the current user
   */
  async getAllTasks(): Promise<Task[]> {
    return apiRequest<Task[]>("/tasks/")
  },

  /**
   * Get a specific task by ID
   */
  async getTaskById(id: number): Promise<Task> {
    return apiRequest<Task>(`/tasks/${id}`)
  },

  /**
   * Create a new task
   */
  async createTask(data: CreateTaskRequest): Promise<Task> {
    return apiRequest<Task>("/tasks/", {
      method: "POST",
      body: JSON.stringify(data),
    })
  },

  /**
   * Update an existing task
   */
  async updateTask(id: number, data: UpdateTaskRequest): Promise<Task> {
    return apiRequest<Task>(`/tasks/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    })
  },

  /**
   * Delete a task
   */
  async deleteTask(id: number): Promise<void> {
    return apiRequest<void>(`/tasks/${id}`, {
      method: "DELETE",
    })
  },

  /**
   * Toggle task completion status
   */
  async toggleCompletion(id: number): Promise<Task> {
    return apiRequest<Task>(`/tasks/${id}/toggle`, {
      method: "PATCH",
    })
  },
}
