import os
from utils.config_reader import get_environment_config

REQUIRED_SECRETS = ["ENV"]

def check_env():
    env = os.getenv("ENV")

    if env not in ["dev", "staging", "prod"]:
        raise Exception(f"Invalid ENV: {env}")

def check_required_secrets():
    missing = []

    for key in REQUIRED_SECRETS:
        if not os.getenv(key):
            missing.append(key)

    if missing:
        raise Exception(f"Missing secrets: {missing}")

def check_config_schema():
    config = get_environment_config()

    required_keys = ["api_url", "base_url", "api"]

    for key in required_keys:
        if key not in config:
            raise Exception(f"Missing config key: {key}")
        