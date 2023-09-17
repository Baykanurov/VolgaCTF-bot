from ...worker import celery
from .. import tasks_process, worksheet


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(25, send_tasks.s())


@celery.task
def send_tasks(*args, **kwargs):
    result = tasks_process.send_message(worksheet)
    return result
