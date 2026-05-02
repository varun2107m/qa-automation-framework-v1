import os
import pytest
from playwright.sync_api import sync_playwright, Page
from typing import Generator
from api.client import APIClient
from utils.config_reader import get_environment_config
from utils.logger import get_logger

from utils.startup_validator import (
    check_env,
    check_required_secrets,
    check_config_schema
)

logger = get_logger(__name__)


# ───────────────────────────────────────────────────────────
# 🚀 Startup Validation
# ───────────────────────────────────────────────────────────
def pytest_sessionstart(session):
    logger.info("Running startup validations...")
    check_env()
    check_required_secrets()
    check_config_schema()
    logger.info("Startup validation completed successfully.")


# ───────────────────────────────────────────────────────────
# 🌐 Browser Fixtures
# ───────────────────────────────────────────────────────────
@pytest.fixture(scope="session")
def browser_instance():
    config = get_environment_config()

    browser_type = config.get("browser", {}).get("type", "chromium")

    is_ci = os.getenv("CI", "false").lower() == "true"
    env_headless = os.getenv("HEADLESS")
    config_headless = config.get("browser", {}).get("headless", True)

    if is_ci:
        headless = True
    elif env_headless is not None:
        headless = env_headless.lower() == "true"
    else:
        headless = config_headless

    logger.info(f"Launching {browser_type} | headless={headless} | CI={is_ci}")

    with sync_playwright() as p:
        browser = getattr(p, browser_type).launch(headless=headless)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser_instance) -> Generator[Page, None, None]:
    context = browser_instance.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()


# ───────────────────────────────────────────────────────────
# 🔌 API Fixtures
# ───────────────────────────────────────────────────────────
@pytest.fixture(scope="session")
def api_client() -> APIClient:
    logger.info("Creating API client instance")
    return APIClient()


# ───────────────────────────────────────────────────────────
# 📦 Shared State
# ───────────────────────────────────────────────────────────
@pytest.fixture(scope="function")
def response_store() -> dict:
    return {}


