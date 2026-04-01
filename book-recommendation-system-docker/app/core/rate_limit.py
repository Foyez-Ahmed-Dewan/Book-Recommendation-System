import time
from collections import defaultdict

from fastapi import Request
from fastapi.responses import JSONResponse

requests_log = defaultdict(list)

RATE_LIMIT = 5
RATE_WINDOW = 10


async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    current_time = time.time()

    requests_log[client_ip] = [
        ts for ts in requests_log[client_ip]
        if current_time - ts < RATE_WINDOW
    ]

    if len(requests_log[client_ip]) >= RATE_LIMIT:
        return JSONResponse(
            status_code=429,
            content={
                "detail": f"Rate limit exceeded. Max {RATE_LIMIT} requests in {RATE_WINDOW} seconds."
            }
        )

    requests_log[client_ip].append(current_time)
    return await call_next(request)