# Library Imports
from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler

# App imports
from app.config import settings

r = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
q = Queue(settings.REDIS_QUEUE, connection=r)
s = Scheduler(settings.REDIS_QUEUE, connection=r)
