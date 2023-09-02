import datetime
from gspread import Worksheet
from .models import Task, Status


def check_task(task: Task):
    if (task.time == datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
            and task.status == Status.waiting.value):
        return True
    else:
        return False


def update_status(worksheet: Worksheet, task: Task):
    worksheet.update(f'D{worksheet.find(task.time).row}', Status.shipped.value)



