from fastapi import FastAPI

from app.router import router


app = FastAPI(
    title="Document Review API"
)
app.include_router(router)