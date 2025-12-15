/**
 * Home page - Landing page with CTA
 * Task: T-031 - Create Home Page with CTA
 */

import Link from "next/link"

export default function HomePage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600">
      <div className="text-center text-white p-8">
        <h1 className="text-5xl font-bold mb-4">Todo App</h1>
        <p className="text-xl mb-8">
          Your tasks, organized. Simple and powerful task management.
        </p>

        <div className="flex gap-4 justify-center">
          <Link
            href="/login"
            className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition"
          >
            Login
          </Link>
          <Link
            href="/register"
            className="bg-transparent border-2 border-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition"
          >
            Register
          </Link>
        </div>
      </div>
    </div>
  )
}
