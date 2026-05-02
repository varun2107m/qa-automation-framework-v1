import json
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from api.client import APIClient
from utils.schema_validator import validate_schema
from utils.logger import get_logger
from utils.assertions import assert_status_code, assert_true
from pathlib import Path

logger = get_logger(__name__)

scenarios("../../features/api/user.feature")

DATA = json.loads(
    (Path("test_data/api/user_data.json")).read_text()
)

# ── Fixtures ────────────────────────────────────────────────
@pytest.fixture
def api_client() -> APIClient:
    return APIClient()

@pytest.fixture
def response():
    return {"value": None}

# ── Steps ───────────────────────────────────────────────────
@given("the API client is ready")
def client_ready(api_client: APIClient) -> None:
    assert_true(api_client is not None, "API client not initialized")

@when(parsers.parse("I request user with id {user_id:d}"))
def get_user(api_client: APIClient, response: dict, user_id: int) -> None:
    logger.info(f"Requesting user with id: {user_id}")
    response["value"] = api_client.get(f"/users/{user_id}")

@then(parsers.parse("response status should be {status:d}"))
def check_status(response: dict, status: int) -> None:
    assert_status_code(response["value"], status)

@then("response should match user schema")
def check_schema(response: dict) -> None:
    res = response["value"]

    if res.status_code == 200:
        validate_schema(res.json(), "user_schema.json")
        

