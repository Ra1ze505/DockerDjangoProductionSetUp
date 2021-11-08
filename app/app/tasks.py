from app.celery import app

import logging

logger = logging.getLogger(__name__)


@app.task
def custom_sum(a, b):
    return a + b

