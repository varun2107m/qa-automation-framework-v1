import json
import jsonschema
from pathlib import Path
from utils.logger import get_logger

logger = get_logger(__name__)

_schema_cache: dict = {}

def validate_schema(response_json: dict, schema_file: str) -> None:
    if schema_file not in _schema_cache:
        path = Path("schemas") / schema_file
        if not path.exists():
            raise FileNotFoundError(f"Schema not found: {path}")
        _schema_cache[schema_file] = json.loads(path.read_text())
        logger.info(f"Schema loaded and cached: {schema_file}")

    schema = _schema_cache[schema_file]

    try:
        jsonschema.validate(instance=response_json, schema=schema)
        logger.info(f"Schema validation passed: {schema_file}")
    except jsonschema.ValidationError as e:
        logger.error(f"Schema validation failed: {e.message}")
        raise
