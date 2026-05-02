import os
import requests
import time
import json
import jsonschema
from requests import Response, Session
from utils.config_reader import get_environment_config
from utils.logger import get_logger
from pathlib import Path
from utils.assertions import assert_status_code

try:
    import allure
    ALLURE_AVAILABLE = True
except ImportError:
    ALLURE_AVAILABLE = False

logger = get_logger(__name__)


class APIClient:
    def __init__(self) -> None:
        config = get_environment_config()

        self.base_url = config["api_url"].rstrip("/")

        api_config = config.get("api", {})
        self.timeout = api_config.get("timeout", 10)
        self.retry_count = api_config.get("retry_count", 2)
        self.retry_delay = api_config.get("retry_delay", 1)

        self.session: Session = requests.Session()

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        headers.update(config.get("headers", {}))

        api_key = os.getenv("REQRES_API_KEY") or os.getenv("API_KEY")
        if api_key and api_key.strip():
            headers["x-api-key"] = api_key.strip()
            logger.info("API key loaded successfully")
        else:
            logger.warning("REQRES_API_KEY not set — requests may return 401")

        self.session.headers.update(headers)
        self._schema_cache = {}

    # ── Core Request Handler ────────────────────────────────
    def _request(self, method: str, endpoint: str, **kwargs) -> Response:
        url = self._url(endpoint)

        for attempt in range(self.retry_count + 1):
            try:
                payload = kwargs.get("json") or kwargs.get("params")
                logger.info(
                    f"{method.upper()} {url} | Payload keys: {list(payload.keys()) if payload else 'None'}"
                )

                response = self.session.request(
                    method=method,
                    url=url,
                    timeout=self.timeout,
                    **kwargs
                )

                self._log_response(response)

                if response.status_code >= 500:
                    logger.warning(f"Server error {response.status_code}, retrying ({attempt + 1})...")
                    if attempt == self.retry_count:
                        return response
                    time.sleep(self.retry_delay)
                    continue

                return response

            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt == self.retry_count:
                    raise
                time.sleep(self.retry_delay)

    # ── HTTP Methods ────────────────────────────────────────
    def get(self, endpoint: str, params: dict | None = None) -> Response:
        return self._request("get", endpoint, params=params)

    def post(self, endpoint: str, payload: dict | None = None) -> Response:
        return self._request("post", endpoint, json=payload)

    def put(self, endpoint: str, payload: dict | None = None) -> Response:
        return self._request("put", endpoint, json=payload)

    def delete(self, endpoint: str) -> Response:
        return self._request("delete", endpoint)

    # ── Helpers ─────────────────────────────────────────────
    def _url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def _log_response(self, response: Response) -> None:
        body_preview = response.text[:300]
        logger.info(f"Response [{response.status_code}] | URL: {response.url} | Body: {body_preview}")

        if ALLURE_AVAILABLE:
            content_type = response.headers.get("Content-Type", "")
            attachment_type = (
                allure.attachment_type.JSON
                if "application/json" in content_type
                else allure.attachment_type.TEXT
            )
            allure.attach(body_preview, name="response", attachment_type=attachment_type)

    def get_json(self, response: Response) -> dict:
        try:
            return response.json()
        except Exception:
            logger.error(f"Invalid JSON response: {response.text}")
            raise

    def validate_schema(self, response: Response, schema_file: str) -> None:
        if schema_file not in self._schema_cache:
            path = Path("schemas") / schema_file
            self._schema_cache[schema_file] = json.loads(path.read_text())

        schema = self._schema_cache[schema_file]
        response_json = response.json()

        try:
            if (
                "data" in response_json
                and "properties" in schema
                and "data" in schema["properties"]
            ):
                jsonschema.validate(
                    instance=response_json["data"],
                    schema=schema["properties"]["data"]
                )
                logger.info(f"Schema validation passed (data only): {schema_file}")
            else:
                jsonschema.validate(instance=response_json, schema=schema)
                logger.info(f"Schema validation passed (full): {schema_file}")

        except jsonschema.ValidationError as e:
            logger.error(f"Schema validation failed: {e.message}")
            raise

    # ── Auth Helpers ────────────────────────────────────────
    def set_token(self, token: str) -> None:
        logger.info("Setting auth token")
        self.session.headers["Authorization"] = f"Bearer {token}"

    def clear_token(self) -> None:
        logger.info("Clearing auth token")
        self.session.headers.pop("Authorization", None)
        
             








    