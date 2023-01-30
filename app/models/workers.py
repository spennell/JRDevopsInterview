from pydantic import BaseModel
from typing import Optional


class WorkersStatus(BaseModel):
    healthy: bool
    scheduler: bool
    worker: bool


class WorkersStatusResponse(BaseModel):
    data: WorkersStatus
    message: Optional[str]
    status: bool
