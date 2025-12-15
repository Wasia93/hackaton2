/**
 * Task statistics component
 * Task: T-033 - Add Task Statistics Component
 */

import { Task } from "@/types/task"

interface TaskStatsProps {
  tasks: Task[]
}

export default function TaskStats({ tasks }: TaskStatsProps) {
  const total = tasks.length
  const completed = tasks.filter((t) => t.completed).length
  const incomplete = total - completed
  const percentage = total > 0 ? Math.round((completed / total) * 100) : 0

  return (
    <div className="bg-white p-6 rounded-lg shadow mb-6">
      <h2 className="text-xl font-bold mb-4">Statistics</h2>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="text-center p-4 bg-blue-50 rounded-lg">
          <div className="text-3xl font-bold text-blue-600">{total}</div>
          <div className="text-sm text-gray-600 mt-1">Total Tasks</div>
        </div>

        <div className="text-center p-4 bg-green-50 rounded-lg">
          <div className="text-3xl font-bold text-green-600">{completed}</div>
          <div className="text-sm text-gray-600 mt-1">Completed</div>
        </div>

        <div className="text-center p-4 bg-yellow-50 rounded-lg">
          <div className="text-3xl font-bold text-yellow-600">{incomplete}</div>
          <div className="text-sm text-gray-600 mt-1">Incomplete</div>
        </div>

        <div className="text-center p-4 bg-purple-50 rounded-lg">
          <div className="text-3xl font-bold text-purple-600">{percentage}%</div>
          <div className="text-sm text-gray-600 mt-1">Progress</div>
        </div>
      </div>

      {total > 0 && (
        <div className="mt-4">
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div
              className="bg-green-500 h-3 rounded-full transition-all duration-300"
              style={{ width: `${percentage}%` }}
            ></div>
          </div>
        </div>
      )}
    </div>
  )
}
