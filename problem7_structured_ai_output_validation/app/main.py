from fastapi import FastAPI

from app.routes.tickets import router

app = FastAPI()
app.include_router(router)
