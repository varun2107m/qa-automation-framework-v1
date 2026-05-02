import json
import pytest
from pytest_bdd import scenarios, given, when, then
from pages.login_page import LoginPage
from utils.config_reader import get_environment_config
from utils.logger import get_logger
from pathlib import Path

logger = get_logger(__name__)

scenarios("../../features/ui/login.feature")


# ── Fixtures ───────────────────────────────────────────────

@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def test_data():
    path = Path("test_data/ui/login_data.json")
    return json.loads(path.read_text())


@pytest.fixture
def env():
    return get_environment_config()


# ── Steps ───────────────────────────────────────────────────

@given("user is on login page")
def open_login(login_page, env):
    logger.info("Opening login page")
    login_page.open(env["base_url"])


@when("user logs in with invalid credentials")
def invalid_login(login_page, test_data):
    user = test_data["invalid_user"]
    logger.info("Logging in with invalid credentials")
    login_page.login(user["username"], user["password"])


@then("error message should be displayed")
def validate_error(login_page, test_data):
    expected = test_data["expected_errors"]["invalid_credentials"]
    logger.info(f"Validating error message: {expected}")
    login_page.assert_error(expected)
    

