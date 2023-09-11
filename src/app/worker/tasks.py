from ...worker import celery
from .. import telegram_response, worksheet


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(25, send_tasks.s())


@celery.task
def send_tasks(*args, **kwargs):
    result = telegram_response.send_message(worksheet)
    return result
