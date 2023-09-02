from celery import Celery


celery = Celery('app',
                broker='redis://redis:6379',
                backend='redis://redis:6379',
                include=['src.app.worker.tasks'])

if __name__ == '__main__':
    celery.start()
