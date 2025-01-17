from locust import HttpUser, task, between, events
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KeyValueUser(HttpUser):
    wait_time = between(1, 2)
    unique_key = f"test_key_{uuid.uuid4()}"
    headers = None  

    def on_start(self):
        try:
            resp = self.client.post("/auth/login", data={
                "username": "sureboy@gmail.com",
                "password": "xxxxxx"
            })
            if resp.status_code == 200:
                try:
                    self.token = resp.json().get("access_token")
                    self.headers = {"Authorization": f"Bearer {self.token}"}
                    logger.info("Login successful.")
                except Exception as e:
                    logger.error(f"Failed to decode login response: {e}")
                    self.headers = None
            else:
                logger.error(f"Login failed: {resp.status_code}, {resp.text}")
                self.headers = None
        except Exception as e:
            logger.error(f"Login request failed: {e}")
            self.headers = None

    @task(3)
    def upsert_key(self):
        if not self.headers:
            logger.warning("Skipping upsert_key task as headers are not set.")
            return
        try:
            resp = self.client.put(
                "/kv/",
                headers=self.headers,
                json={
                    "key": self.unique_key,
                    "value": "some_value",
                    "ttl": 60
                }
            )
            if resp.status_code == 200:
                logger.info(f"Upsert successful for key '{self.unique_key}'.")
            else:
                logger.error(f"Upsert failed: {resp.status_code}, {resp.text}")
        except Exception as e:
            logger.error(f"Upsert request failed: {e}")

    @task(2)
    def read_key(self):
        if not self.headers:
            logger.warning("Skipping read_key task as headers are not set.")
            return
        try:
            resp = self.client.get(f"/kv/{self.unique_key}", headers=self.headers)
            if resp.status_code == 200:
                try:
                    logger.info(f"Read key '{self.unique_key}': {resp.json()}")
                except Exception as e:
                    logger.error(f"Failed to decode read response: {e}")
            else:
                logger.warning(f"Failed to read key (maybe not created yet?): {resp.status_code}, {resp.text}")
        except Exception as e:
            logger.error(f"Read request failed: {e}")

    @task(1)
    def delete_key(self):
        if not self.headers:
            logger.warning("Skipping delete_key task as headers are not set.")
            return
        try:
            resp = self.client.delete(f"/kv/{self.unique_key}", headers=self.headers)
            if resp.status_code == 200:
                logger.info(f"Deleted key '{self.unique_key}' (or it was absent).")
            else:
                logger.warning(f"Delete failed: {resp.status_code}, {resp.text}")
        except Exception as e:
            logger.error(f"Delete request failed: {e}")

    def on_stop(self):
        if self.headers:
            try:
                resp = self.client.delete(f"/kv/{self.unique_key}", headers=self.headers)
                if resp.status_code == 200:
                    logger.info(f"Cleanup: Deleted key '{self.unique_key}'.")
                else:
                    logger.warning(f"Cleanup: Delete key failed: {resp.status_code}, {resp.text}")
            except Exception as e:
                logger.error(f"Cleanup request failed: {e}")


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    logger.info("Load test started.")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    logger.info("Load test stopped.")
