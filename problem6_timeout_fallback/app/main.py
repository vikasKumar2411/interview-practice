from fastapi import FastAPI

from app.routes.descriptions import router

app = FastAPI()
app.include_router(router)
