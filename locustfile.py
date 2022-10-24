import os
import pickle

from lightning.app import LightningFlow
from locust import FastHttpUser, task
from locust.log import setup_logging

setup_logging("INFO", None)

queue_url = os.getenv("LIGHTNING_HTTP_QUEUE_URL")
if queue_url is None:
    raise ValueError("LIGHTNING_HTTP_QUEUE_URL is not set")


class TestFlow(LightningFlow):
    pass


pickled_work = pickle.dumps(TestFlow())

long_json = pickle.dumps({k: str(k) for k in range(100000)})

# use jwt CLI tool to generate the token with the right signing key
# jwt encode  --secret <signing-key-can-be-found-in-gridlet/bifrost-env> --payload "app_id=test-app" --alg HS512|
headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJhcHBfaWQiOiJ0ZXN0LWFwcCIsImlhdCI6MTY2NjU5NzA3Mn0.WvxGmz3eyNHG3_JJGqx-tZjfOvMpr4NS6HUme_oPg-EcTX9yamlcvPyjqZkJYMVPbSFt52uAxDROLaXKpldbHw"}


class User(FastHttpUser):

    host = queue_url

    @task(131)
    def api_response_queue(self):
        self.client.post("/v1/test-app/API_RESPONSE_QUEUE", params={"action": "pop"}, headers=headers)

    @task(57)
    def api_delta_queue(self):
        self.client.post("/v1/test-app/API_DELTA_QUEUE", params={"action": "pop"}, headers=headers)

    @task(57)
    def delta_queue(self):
        self.client.post("/v1/test-app/DELTA_QUEUE", params={"action": "pop"}, headers=headers)

    @task(131)
    def api_state_publish_queue(self):
        self.client.post("/v1/test-app/API_STATE_PUBLISH_QUEUE", params={"action": "pop"}, headers=headers)

    @task(58)
    def error_queue(self):
        self.client.post("/v1/test-app/ERROR_QUEUE", params={"action": "pop"}, headers=headers)

    @task(54)
    def orchestrator_copy_response_work1(self):
        self.client.post("/v1/test-app/ORCHESTRATOR_COPY_RESPONSE_work1", params={"action": "pop"}, headers=headers)

    @task(54)
    def orchestrator_copy_response_work2(self):
        self.client.post("/v1/test-app/ORCHESTRATOR_COPY_RESPONSE_work2", params={"action": "pop"}, headers=headers)

    @task(182)
    def orchestrator_copy_request_work1(self):
        self.client.post("/v1/test-app/ORCHESTRATOR_COPY_REQUEST_work1", params={"action": "pop"}, headers=headers)

    @task(182)
    def orchestrator_copy_request_work2(self):
        self.client.post("/v1/test-app/ORCHESTRATOR_COPY_REQUEST_work2", params={"action": "pop"}, headers=headers)

    @task(53)
    def orchestrator_request_work1(self):
        self.client.post("/v1/test-app/ORCHESTRATOR_REQUEST_work1", params={"action": "pop"}, headers=headers)

    @task(54)
    def orchestrator_request_work2(self):
        self.client.post("/v1/test-app/ORCHESTRATOR_REQUEST_work2", params={"action": "pop"}, headers=headers)

    @task(183)
    def caller_queue_work1(self):
        self.client.post("/v1/test-app/CALLER_QUEUE_work1", params={"action": "pop"}, headers=headers)

    @task(183)
    def caller_queue_work2(self):
        self.client.post("/v1/test-app/CALLER_QUEUE_work2", params={"action": "pop"}, headers=headers)

    @task(5)
    def caller_queue_work1_push(self):
        self.client.post("/v1/test-app/CALLER_QUEUE_work1", params={"action": "push"}, data=pickled_work, headers=headers)

    @task(5)
    def delta_queue_push(self):
        self.client.post("/v1/test-app/DELTA_QUEUE", params={"action": "push"}, data=long_json, headers=headers)

    @task(10)
    def orchestrator_copy_request_work2_push(self):
        self.client.post("/v1/test-app/ORCHESTRATOR_COPY_REQUEST_work2", params={"action": "push"}, data=pickled_work, headers=headers)

    @task(10)
    def orchestrator_copy_request_work1_push(self):
        self.client.post("/v1/test-app/ORCHESTRATOR_COPY_REQUEST_work1", params={"action": "push"}, data=pickled_work, headers=headers)
