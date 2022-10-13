import os

from locust import HttpUser, task
from locust.log import setup_logging

setup_logging("INFO", None)

queue_url = os.getenv("LIGHTNING_HTTP_QUEUE_URL")
if queue_url is None:
    raise ValueError("LIGHTNING_HTTP_QUEUE_URL is not set")


class User(HttpUser):

    host = queue_url

    @task
    def my_task(self):
        self.client.get("/v1/test-queue/test-app/length")
