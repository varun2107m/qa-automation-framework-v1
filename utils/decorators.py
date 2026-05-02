from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from utils.logger import get_logger

logger = get_logger(__name__)

def handle_timeout(action_name):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except PlaywrightTimeoutError as e:
                logger.error(f"{action_name} failed")
                self.take_screenshot(f"{action_name}_failure")
                raise AssertionError(f"{action_name} failed") from e
        return wrapper
    return decorator
