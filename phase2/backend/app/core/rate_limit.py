"""
Rate limiting middleware for FastAPI
Phase II: Request rate limiting
"""

import time
from collections import defaultdict
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    In-memory sliding window rate limiter.
    Limits requests per IP address.
    """

    def __init__(self, app, default_limit: int = 100, auth_limit: int = 20, window_seconds: int = 60):
        super().__init__(app)
        self.default_limit = default_limit
        self.auth_limit = auth_limit
        self.window_seconds = window_seconds
        self.requests: dict[str, list[float]] = defaultdict(list)

    def _get_client_ip(self, request: Request) -> str:
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    def _clean_old_requests(self, key: str, now: float):
        cutoff = now - self.window_seconds
        self.requests[key] = [t for t in self.requests[key] if t > cutoff]

    async def dispatch(self, request: Request, call_next) -> Response:
        # Skip rate limiting for health checks
        if request.url.path in ("/health", "/"):
            return await call_next(request)

        client_ip = self._get_client_ip(request)
        now = time.time()

        # Determine limit based on path
        is_auth = request.url.path.startswith("/auth")
        limit = self.auth_limit if is_auth else self.default_limit
        key = f"{client_ip}:{'auth' if is_auth else 'general'}"

        self._clean_old_requests(key, now)
        current_count = len(self.requests[key])
        remaining = max(0, limit - current_count)
        reset_time = int(now + self.window_seconds)

        if current_count >= limit:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Please try again later."},
                headers={
                    "X-RateLimit-Limit": str(limit),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(reset_time),
                    "Retry-After": str(self.window_seconds),
                },
            )

        self.requests[key].append(now)
        response = await call_next(request)

        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining - 1)
        response.headers["X-RateLimit-Reset"] = str(reset_time)

        return response
