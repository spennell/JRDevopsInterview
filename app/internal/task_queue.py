# Library Imports
from datetime import datetime
from redis import Redis
from rq_scheduler import Scheduler
from rq import Queue
from rq.worker import Worker

# App Imports
from app.config import settings
from app.db.rq_db import q, r, s


class Jobs:
    @staticmethod
    def cancel_scheduled_jobs():
        for job in s.get_jobs():
            print("Canceling: ", job)
            s.cancel(job)

    @staticmethod
    def schedule_job(interval: int, func, args=None):
        return s.schedule(
            scheduled_time=datetime.utcnow(),
            func=func,
            args=args,
            interval=interval * 60,
            repeat=None
        )

    @staticmethod
    def scheduled_jobs():
        return s.get_jobs()

    @staticmethod
    def queue_job(func):
        job = q.enqueue_job(func)
        return job

    @staticmethod
    def test_con():
        try:
            r.ping()
            return True
        except Exception as e:
            print(str(e))
            return False


class Workers:
    @staticmethod
    def list():
        workers = Worker.all(r)
        return workers

    @staticmethod
    def scheduler_id():
        scheduler = Scheduler(settings.REDIS_QUEUE, connection=r)
        return scheduler.pid
