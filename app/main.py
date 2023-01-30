from fastapi import FastAPI
from app.api.workers import api as worker_api

app = FastAPI()

app.include_router(worker_api, prefix="/workers", tags=["workers"])

