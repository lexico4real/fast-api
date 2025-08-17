import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from configs.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log incoming request
        logger.info(
            f"Incoming request: {request.method} {request.url.path} "
            f"from {request.client.host}"
        )

        try:
            response = await call_next(request)
        except Exception as exc:
            # If something goes really wrong before reaching handlers
            logger.error(
                f"Unhandled error during request {request.method} {request.url.path}: {exc}",
                exc_info=True,
            )
            raise

        # Response time
        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"Completed {request.method} {request.url.path} "
            f"with status {response.status_code} in {process_time:.2f}ms"
        )

        return response
