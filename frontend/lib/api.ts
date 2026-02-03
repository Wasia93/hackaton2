/**
 * API client utility for backend communication
 * Task: T-019 - Create API Client Utility
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

/**
 * Make an authenticated API request to the backend.
 * Automatically includes JWT token from localStorage if available.
 *
 * @param endpoint - API endpoint path (e.g., "/tasks/")
 * @param options - Fetch options (method, body, headers, etc.)
 * @returns Promise with parsed JSON response
 */
export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  // Get JWT token from localStorage (set by Better Auth)
  const token = typeof window !== "undefined"
    ? localStorage.getItem("auth_token")
    : null

  // Build headers (use Record<string, string> for indexable access)
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  }

  // Add authorization header if token exists
  if (token) {
    headers["Authorization"] = `Bearer ${token}`
  }

  // Make request
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  })

  // Handle authentication errors
  if (response.status === 401) {
    // Clear token and redirect to login
    if (typeof window !== "undefined") {
      localStorage.removeItem("auth_token")
      window.location.href = "/login"
    }
    throw new Error("Unauthorized")
  }

  // Handle other errors
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || `API error: ${response.statusText}`)
  }

  // Return parsed JSON for non-204 responses
  if (response.status === 204) {
    return undefined as T
  }

  return response.json()
}
