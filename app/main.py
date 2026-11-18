from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app import models
from app.database import Base, engine
from app.routers import ALL_ROUTERS

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Corporate Learning REST API",
    description="Практическая работа №8 (вариант 28): REST API с CRUD, "
    "бизнес-логикой и валидацией. Блок Е — корпоративное обучение.",
    version="1.0.0",
)

for router in ALL_ROUTERS:
    app.include_router(router)


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(status_code=404, content={"detail": "Resource not found"})


@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Validation error", "errors": exc.errors()},
    )


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}


@app.get("/", tags=["meta"])
def root():
    return {
        "message": "Corporate Learning REST API",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }