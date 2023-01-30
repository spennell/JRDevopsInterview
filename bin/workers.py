import subprocess
import sys
import typer

from pathlib import Path
from redis import Redis
from rich import print
from rq import Queue
from rq.command import send_shutdown_command
from rq_scheduler import Scheduler
from rq.worker import Worker


sys.path.insert(0, f"{Path(__file__).parents[1]}")
from app.config import settings

cli = typer.Typer()


class Workers:
    r = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    q = Queue(settings.REDIS_QUEUE, connection=r)

    def list(self):
        workers = Worker.all(self.r)
        return workers

    def scheduler_id(self):
        scheduler = Scheduler(settings.REDIS_QUEUE, connection=self.r)
        return scheduler.pid

    @staticmethod
    def start():
        subprocess.Popen([
            "rq", "worker", "-c", "rq_worker"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=f"{Path(__file__).parents[1]}/app")

        pgrep_out = subprocess.Popen(["pgrep", "-f", "rq_worker"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = pgrep_out.communicate()
        if stdout:
            pid = stdout.decode("utf-8").strip()
            if pid:
                print(f"[bold magenta]INFO:[/bold magenta] rq worker started as PID: {pid}")
            else:
                print(f"[bold red]ERROR:[/bold red] failed to start rq worker")

        subprocess.Popen([
            "rqscheduler", "-H", f"{settings.REDIS_HOST}", "-p", f"{settings.REDIS_PORT}", "-d", f"{settings.REDIS_DB}"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        pgrep_out = subprocess.Popen(["pgrep", "-f", "rqscheduler"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = pgrep_out.communicate()
        if stdout:
            pid = stdout.decode("utf-8").strip()
            if pid:
                print(f"[bold magenta]INFO:[/bold magenta] rqscheduler started as PID: {pid}")
            else:
                print(f"[bold red]ERROR:[/bold red] failed to start rqscheduler")

    def stop(self):
        for worker in Worker.all(self.r):
            print(f"[bold yellow]WARNING:[/bold yellow] Stopped worker {worker.name}")
            send_shutdown_command(self.r, worker.name)

        pgrep_out = subprocess.Popen(["pgrep", "-f", "rqscheduler"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = pgrep_out.communicate()
        if stdout:
            pid = stdout.decode('utf-8').strip()
            if pid:
                print(f"[bold yellow]WARNING:[/bold yellow] Stopped scheduler")
                subprocess.Popen(["kill", pid])


@cli.command()
def restart():
    workers = Workers()
    workers.stop()
    workers.start()


@cli.command()
def start():
    print("[bold cyan]INFO:[/bold cyan] Attempting to start workers")
    Workers.start()


@cli.command()
def stop():
    print("[bold cyan]INFO:[/bold cyan] Attempting to stop workers")
    workers = Workers()
    workers.stop()


@cli.command()
def status():
    workers = Workers()

    worker_list = workers.list()
    rq_scheduler = workers.scheduler_id()

    if worker_list:
        print(f"[bold cyan]INFO:[/bold cyan] RQ Worker is [green]online[/green].")
    else:
        print("[bold red]ERROR:[/bold red] RQ Worker is [red]offline[/red].")

    if rq_scheduler:
        print(f"[bold cyan]INFO:[/bold cyan] RQ Scheduler is [green]online[/green].")
    else:
        print("[bold red]ERROR:[/bold red] RQ Scheduler is [red]offline[/red].")


if __name__ == "__main__":
    cli()
