/**
 * Protected route wrapper with authentication check
 * Task: T-023 - Create Protected Route Wrapper
 */

"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"

interface ProtectedRouteProps {
  children: React.ReactNode
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    const checkAuth = () => {
      // Check if JWT token exists in localStorage
      const token = localStorage.getItem("auth_token")

      if (!token) {
        // No token, redirect to login
        router.push("/login")
        return
      }

      // TODO: Validate token with backend when Better Auth is implemented
      // For now, just check if token exists
      setIsAuthenticated(true)
      setIsLoading(false)
    }

    checkAuth()
  }, [router])

  // Show loading state while checking authentication
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  // If not authenticated, don't render anything (redirecting)
  if (!isAuthenticated) {
    return null
  }

  // User is authenticated, render children
  return <>{children}</>
}
