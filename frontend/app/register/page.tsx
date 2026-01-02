/**
 * Registration page
 * Task: T-022 - Create Registration Page
 */

"use client"

import { useState, FormEvent } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"

export default function RegisterPage() {
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError("")

    if (password.length < 8) {
      setError("Password must be at least 8 characters")
      return
    }

    setIsLoading(true)

    try {
      // Call backend register endpoint to get valid JWT token
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

      const response = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      })

      if (!response.ok) {
        const error = await response.json().catch(() => ({}))
        throw new Error(error.detail || "Registration failed")
      }

      const data = await response.json()

      // Store the valid JWT token from backend
      localStorage.setItem("auth_token", data.access_token)
      localStorage.setItem("user_id", data.user_id)
      localStorage.setItem("user_email", email)

      // Redirect to dashboard
      router.push("/dashboard")
    } catch (err: any) {
      setError(err.message || "Registration failed. Email may already exist.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="max-w-md w-full p-6 bg-white rounded-lg shadow">
        <h1 className="text-2xl font-bold mb-6">Register</h1>

        {error && (
          <div className="bg-red-100 text-red-700 p-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block mb-2 font-semibold">Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full border p-2 rounded"
              required
              disabled={isLoading}
            />
          </div>

          <div className="mb-4">
            <label className="block mb-2 font-semibold">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full border p-2 rounded"
              required
              disabled={isLoading}
            />
          </div>

          <div className="mb-4">
            <label className="block mb-2 font-semibold">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full border p-2 rounded"
              required
              minLength={8}
              disabled={isLoading}
            />
            <p className="text-sm text-gray-600 mt-1">
              Minimum 8 characters
            </p>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600 disabled:bg-gray-400 transition"
          >
            {isLoading ? "Registering..." : "Register"}
          </button>
        </form>

        <p className="mt-4 text-center">
          Already have an account?{" "}
          <Link href="/login" className="text-blue-500 hover:underline">
            Login
          </Link>
        </p>
      </div>
    </div>
  )
}
