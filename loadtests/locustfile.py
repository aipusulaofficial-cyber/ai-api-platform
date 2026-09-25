from locust import HttpUser, task, between


class APIUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def domain(self):
        self.client.post(
            "/v1/api",
            json={
                "key": "load",
                "payload": {
                    "text": "load",
                    "query": "load",
                    "value": 1,
                    "timestamp": 1,
                    "steps": ["a"],
                    "cases": [],
                    "owner": "load",
                    "actor": "load",
                    "classification": "public",
                    "required_classification": "public",
                    "version": "v1",
                },
            },
            name="/v1/api",
        )
