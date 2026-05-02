from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):

    URL = "/"

    # Locators
    USERNAME = "#user-name"
    PASSWORD = "#password"
    LOGIN_BTN = "#login-button"
    ERROR = ".error-message-container"

    def open(self, base_url: str) -> None:
        full_url = base_url.rstrip("/") + self.URL
        self.navigate(full_url)
        self.wait_for(self.LOGIN_BTN)   # ensure page is ready
        logger.info("Login page loaded successfully")

    def login(self, username: str, password: str) -> None:
        logger.info("Attempting login")

        self.fill(self.USERNAME, username)
        self.fill(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

    def get_error(self) -> str:
        return self.get_text(self.ERROR)

    def is_error_visible(self) -> bool:
        return self.is_visible(self.ERROR)

    def assert_error(self, expected_msg: str) -> None:
        actual = self.get_error()
        assert expected_msg in actual, f"Expected '{expected_msg}' but got '{actual}'"

    