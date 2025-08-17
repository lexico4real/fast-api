from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from configs.logger import logger


# Handle DB constraint issues (duplicates, FK violations, etc.)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    logger.warning(f"Integrity error at {request.url.path}: {exc}")
    return JSONResponse(
        status_code=400,
        content={"message": "Integrity error: possible duplicate or invalid data."}
    )


# Handle generic SQLAlchemy errors
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    logger.error(
        f"SQLAlchemy error at {request.url.path}: {exc}", exc_info=True
    )
    return JSONResponse(
        status_code=500,
        content={"message": "A database error occurred. Please try again later."}
    )


# Handle HTTPException (FastAPI / Starlette built-in)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.info(
        f"HTTP error {exc.status_code} at {request.url.path}: {exc.detail}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail or "An error occurred."}
    )


# Handle *any* unhandled exception (fallback safety net)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.critical(
        f"Unhandled exception at {request.url.path}", exc_info=True
    )
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error. Please try again later."}
    )
