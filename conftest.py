import pytest
from playwright.sync_api import sync_playwright, Page
from typing import Generator
from api.client import APIClient
from utils.config_reader import get_environment_config
from utils.logger import get_logger
import os

from utils.startup_validator import (
    check_env,
    check_required_secrets,
    check_config_schema
)

logger = get_logger(__name__)


# ───────────────────────────────────────────────────────────
# 🚀 Startup Validation (RUNS ONCE BEFORE TEST SESSION)
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

    browser_type = config["browser"].get("type", "chromium")

    # ✅ Priority: ENV → config → default
    env_headless = os.getenv("HEADLESS")
    config_headless = config["browser"].get("headless", True)

    if env_headless is not None:
        headless = env_headless.lower() == "true"
    else:
        headless = config_headless

    # ✅ FORCE headless in CI (critical fix)
    is_ci = os.getenv("CI", "false").lower() == "true"
    if is_ci:
        headless = True

    logger.info(f"Launching {browser_type} | headless={headless}")

    with sync_playwright() as p:
        browser = getattr(p, browser_type).launch(headless=headless)
        yield browser
        browser.close()


@pytest.fixture(scope="function")                    # ← THIS WAS MISSING
def page(browser_instance) -> Page:
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
# 📦 Shared State (if needed for API tests)
# ───────────────────────────────────────────────────────────
@pytest.fixture(scope="function")
def response_store() -> dict:
    return {}

