from playwright.sync_api import Page
from utils.logger import get_logger
from utils.decorators import handle_timeout
from datetime import datetime
from utils.assertions import assert_contains
import os
import allure

logger = get_logger(__name__)


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    # ── Navigation ──────────────────────────────────────────
    def navigate(self, url: str) -> None:
        logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="domcontentloaded")

    # ── Actions ─────────────────────────────────────────────
    @handle_timeout("click")
    def click(self, locator: str, timeout: int = 5000) -> None:
        logger.info(f"Clicking: {locator}")
        self.page.locator(locator).wait_for(state="visible", timeout=timeout)
        self.page.locator(locator).click()

    @handle_timeout("fill")
    def fill(self, locator: str, value: str, timeout: int = 5000) -> None:
        logger.info(f"Filling: {locator} with value: {value}")
        self.page.locator(locator).wait_for(state="visible", timeout=timeout)
        self.page.locator(locator).fill(value)

    @handle_timeout("get_text")
    def get_text(self, locator: str, timeout: int = 5000) -> str:
        self.page.locator(locator).wait_for(state="visible", timeout=timeout)
        text = self.page.locator(locator).text_content()
        logger.info(f"Text from {locator}: {text}")
        return text

    @handle_timeout("wait_for")
    def wait_for(self, locator: str, timeout: int = 5000) -> None:
        logger.info(f"Waiting for: {locator}")
        self.page.locator(locator).wait_for(state="visible", timeout=timeout)

    # ── State Checks ────────────────────────────────────────
    def is_visible(self, locator: str, timeout: int = 5000) -> bool:
        try:
            self.page.locator(locator).wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    # ── Utilities ───────────────────────────────────────────
    def take_screenshot(self, name: str = "screenshot") -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        directory = "reports/screenshots"
        os.makedirs(directory, exist_ok=True)

        file_path = f"{directory}/{name}_{timestamp}.png"
        logger.info(f"Taking screenshot: {file_path}")

        self.page.screenshot(path=file_path)

        # Attach to Allure report
        try:
            allure.attach.file(
                file_path,
                name=name,
                attachment_type=allure.attachment_type.PNG
            )
        except Exception:
            pass
        
    # ── Assertions ──────────────────────────────────────────
def assert_text(self, locator: str, expected: str) -> None:
    actual = self.get_text(locator)
    assert_contains(
        actual,
        expected,
        f"Text mismatch for locator: {locator}"
    )







