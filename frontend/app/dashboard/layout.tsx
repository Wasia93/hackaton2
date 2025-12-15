/**
 * Dashboard layout with navigation and protected route
 * Task: T-024 - Create Dashboard Layout (updated with T-023)
 */

"use client"

import { useRouter } from "next/navigation"
import ProtectedRoute from "@/components/ProtectedRoute"

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()

  const handleLogout = () => {
    localStorage.removeItem("auth_token")
    router.push("/login")
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-white shadow p-4">
          <div className="max-w-7xl mx-auto flex justify-between items-center">
            <h1 className="text-xl font-bold">Todo App - Phase II</h1>
            <button
              onClick={handleLogout}
              className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition"
            >
              Logout
            </button>
          </div>
        </nav>

        <main className="max-w-7xl mx-auto p-6">{children}</main>
      </div>
    </ProtectedRoute>
  )
}
