from pathlib import Path
import json
from typing import Any, Dict

DEFAULT_CONFIG = {
    "LOG_DIR": "./logs",
    "REPORT_DIR": "./reports",
    "REPORT_SIZE": 20,
    "PARSE_ERROR_THRESHOLD": 0.2,
    "LOG_FILE": None,
}

def load_config(path: Path | None) -> Dict[str, Any]:
    config = DEFAULT_CONFIG.copy()
    if path is None:
        return config
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    try:
        with path.open("r", encoding="utf-8") as f:
            file_config = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {path}") from e
    config.update(file_config)
    return config
