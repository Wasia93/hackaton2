/**
 * Task list component
 * Task: T-026 - Create Task List Component
 */

import { Task } from "@/types/task"

interface TaskListProps {
  tasks: Task[]
  onToggle: (id: number) => void
  onEdit: (task: Task) => void
  onDelete: (id: number) => void
}

export default function TaskList({
  tasks,
  onToggle,
  onEdit,
  onDelete,
}: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="text-center text-gray-500 py-8 bg-white rounded-lg shadow">
        No tasks yet. Create your first task above!
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <div
          key={task.id}
          className="bg-white p-4 rounded-lg shadow flex items-start gap-4 hover:shadow-md transition"
        >
          <input
            type="checkbox"
            checked={task.completed}
            onChange={() => onToggle(task.id)}
            className="mt-1 w-5 h-5 cursor-pointer"
            aria-label={`Toggle completion for ${task.title}`}
          />

          <div className="flex-1">
            <h3
              className={`font-semibold text-lg ${
                task.completed ? "line-through text-gray-500" : "text-gray-900"
              }`}
            >
              {task.title}
            </h3>
            {task.description && (
              <p className="text-gray-600 text-sm mt-1">{task.description}</p>
            )}
            <p className="text-xs text-gray-400 mt-2">
              Created: {new Date(task.created_at).toLocaleString()}
            </p>
          </div>

          <div className="flex gap-2">
            <button
              onClick={() => onEdit(task)}
              className="text-blue-500 hover:text-blue-700 px-3 py-1 border border-blue-500 rounded hover:bg-blue-50 transition"
              aria-label={`Edit ${task.title}`}
            >
              Edit
            </button>
            <button
              onClick={() => onDelete(task.id)}
              className="text-red-500 hover:text-red-700 px-3 py-1 border border-red-500 rounded hover:bg-red-50 transition"
              aria-label={`Delete ${task.title}`}
            >
              Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  )
}
