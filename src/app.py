import logging
from time import monotonic

from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from core.settings import get_settings
from core.logger_config import init_logger, LOGGING_CONFIG
from api.cars import router as car_router

init_logger()
settings = get_settings()
logger = logging.getLogger()
app = FastAPI(
    title=settings.PROJECT_NAME,
)

app.include_router(car_router, prefix="/cars", tags=["cars"])


@app.exception_handler(Exception)
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
    uvicorn.run(app, port=8080, log_config=LOGGING_CONFIG)
