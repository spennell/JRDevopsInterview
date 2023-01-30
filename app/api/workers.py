# Library Imports
from fastapi import APIRouter


# App Imports
from app.internal.task_queue import Workers
from app.models.workers import WorkersStatus, WorkersStatusResponse


api = APIRouter()


@api.get("/status", response_model=WorkersStatusResponse)
async def get_worker_status():
    worker_mgr = Workers()
    worker = True if worker_mgr.list() else False
    scheduler = True if worker_mgr.scheduler_id() else False
    healthy = worker and scheduler

    return WorkersStatusResponse(
        data=WorkersStatus(healthy=healthy, scheduler=scheduler, worker=worker),
        status=True
    )
