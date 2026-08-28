"""
Load/stress testing with Locust.
    locust -f load_test.py --host http://localhost:8000
Then open http://localhost:8089.
"""

import random
from locust import HttpUser, task, between


class CoordinatorUser(HttpUser):
    wait_time = between(1, 3)

    @task(5)
    def view_zones(self):
        self.client.get("/api/zones/")

    @task(2)
    def view_root(self):
        self.client.get("/")

    @task(2)
    def predict_demand(self):
        zone_id = random.choice([1, 2, 3])
        self.client.get(f"/api/demand/{zone_id}", name="/api/demand/[id]")

    @task(1)
    def run_allocation(self):
        resource = random.choice(["food", "water", "medical_kit", "shelter_kit"])
        self.client.post("/api/logistics/allocate", json={"resource_type": resource}, name="/api/logistics/allocate")

    @task(1)
    def view_volunteers(self):
        self.client.get("/api/volunteers/")
