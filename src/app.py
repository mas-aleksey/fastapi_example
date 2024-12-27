import logging
from contextlib import asynccontextmanager
from time import monotonic

from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

import controllers.car_controller as car_module
from api.cars import router as car_router
from core.settings import get_settings
from db.connector import DatabaseConnector

settings = get_settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("application startup")
    db = DatabaseConnector(settings.DB.asyncpg_url)
    car_module.controller = car_module.CarController(db)
    yield
    await db.disconnect()
    logger.info("application shutdown")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
)

app.include_router(car_router, prefix="/cars", tags=["cars"])


@app.exception_handler(500)
async def common_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": (
                f"Failed method {request.method} at URL {request.url}."
                f" Exception message is {exc!r}."
            )
        },
    )


@app.middleware("http")
async def time_log_middleware(request, call_next):
    start_time = monotonic()
    try:
        return await call_next(request)
    finally:
        elapsed = 1000.0 * (monotonic() - start_time)
        process_time = "{:0.6f}|ms".format(elapsed)
        logger.info(f"Response: {request.url.path} Duration: {process_time}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000, log_config="core/logging.yaml")
