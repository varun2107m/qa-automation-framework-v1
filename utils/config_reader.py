import yaml
import os
import re
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()


# ── YAML Loader ───────────────────────────────────────────
def load_yaml(file_path: str) -> dict:
    with open(file_path, "r") as file:
        return yaml.safe_load(file) or {}


# ── ENV ───────────────────────────────────────────────────
def get_env() -> str:
    return os.getenv("ENV", "dev")


# ── SAFE ENV RESOLVER ─────────────────────────────────────
def resolve_env_variables(value):
    """
    Replace ${VAR} with actual environment variable
    """
    if isinstance(value, str):
        matches = re.findall(r"\$\{(.*?)\}", value)

        for var in matches:
            env_value = os.getenv(var)

            # ✅ FIX: strict + controlled fallback
            if env_value is None:
                if var in ["API_KEY", "REQRES_API_KEY"]:
                    raise Exception(
                        f"Missing required secret: {var}\n"
                        f"👉 Add it to your .env file or CI secrets"
                    )
                else:
                    env_value = ""   # safe fallback for non-critical vars

            value = value.replace(f"${{{var}}}", env_value)

    return value


# ── RECURSIVE RESOLVER ────────────────────────────────────
def resolve_dict(data):
    if isinstance(data, dict):
        return {k: resolve_dict(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [resolve_dict(i) for i in data]
    else:
        return resolve_env_variables(data)


# ── MERGE LOGIC ───────────────────────────────────────────
def deep_merge(base: dict, override: dict) -> dict:
    result = base.copy()

    for key, value in override.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value

    return result


# ── CONFIG LOADER ─────────────────────────────────────────
@lru_cache()
def load_config() -> dict:
    base_config = load_yaml("config/config.yaml")
    env_config_all = load_yaml("config/environments.yaml")

    env = get_env()

    if env not in env_config_all:
        raise Exception(f"Environment '{env}' not found in environments.yaml")

    env_config = env_config_all[env]

    merged = deep_merge(base_config, env_config)

    resolved = resolve_dict(merged)

    resolved["env"] = env

    return resolved


# ── PUBLIC API ────────────────────────────────────────────
def get_environment_config() -> dict:
    return load_config()


def get_api_key() -> str:
    key = os.getenv("API_KEY")

    if not key:
        raise Exception("API_KEY is missing in environment variables")

    return key




