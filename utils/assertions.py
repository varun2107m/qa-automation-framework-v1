from utils.logger import get_logger

logger = get_logger(__name__)


# ── GENERIC ASSERTIONS ─────────────────────────────────────
def assert_equal(actual, expected, message: str = "") -> None:
    assert actual == expected, (
        message or f"Expected '{expected}', but got '{actual}'"
    )


def assert_not_equal(actual, expected, message: str = "") -> None:
    assert actual != expected, (
        message or f"Did not expect '{expected}', but got '{actual}'"
    )


def assert_true(condition: bool, message: str = "") -> None:
    assert condition, (message or "Condition is not True")


def assert_false(condition: bool, message: str = "") -> None:
    assert not condition, (message or "Condition is not False")


# ── STRING ASSERTIONS ──────────────────────────────────────
def assert_contains(actual: str, expected: str) -> None:
    assert expected in actual, (
        f"Expected '{expected}' to be in '{actual}'"
    )


def assert_not_contains(actual: str, expected: str) -> None:
    assert expected not in actual, (
        f"Did not expect '{expected}' in '{actual}'"
    )


# ── API ASSERTIONS ─────────────────────────────────────────
def assert_status_code(response, expected: int) -> None:
    actual = response.status_code
    assert actual == expected, (
        f"Expected status {expected}, but got {actual}\n"
        f"URL: {response.url}\n"
        f"Response: {response.text}"
    )


def assert_json_key(response_json: dict, key: str) -> None:
    assert key in response_json, (
        f"Key '{key}' not found in response: {response_json}"
    )


def assert_json_value(response_json: dict, key: str, expected) -> None:
    actual = response_json.get(key)
    assert actual == expected, (
        f"Expected '{key}' = '{expected}', but got '{actual}'"
    )


# ── UI ASSERTIONS ──────────────────────────────────────────
def assert_element_visible(is_visible: bool, locator: str) -> None:
    assert is_visible, f"Expected element '{locator}' to be visible"


def assert_text_match(actual: str, expected: str) -> None:
    assert expected in actual, (
        f"Expected text '{expected}', but got '{actual}'"
    )
    