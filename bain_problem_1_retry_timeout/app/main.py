from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.errors import ClassificationUnavailableError

app = FastAPI()
app.include_router(router)

@app.exception_handler(ClassificationUnavailableError)
async def handle_classification_unavailable(
    request: Request,
    exc: ClassificationUnavailableError,
):
    return JSONResponse(
        status_code=503,
        content={"detail": "classification unavailable"},
    )
