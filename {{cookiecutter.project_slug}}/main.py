from fastapi import FastAPI, HTTPException
from configs.database import Base, engine
from controllers import user_controller
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from configs.exception_handlers import (
    integrity_error_handler,
    sqlalchemy_error_handler,
    http_exception_handler,
    generic_exception_handler
)
from middlewares.logging_middleware import LoggingMiddleware

# ⚠️ Prefer Alembic in production
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI • CRUD")

# Middleware
app.add_middleware(LoggingMiddleware)


# Routers
app.include_router(user_controller.router)

# Exception Handlers
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Root Endpoint
@app.get("/")
async def root():
    return {"message": "App Running...!"}