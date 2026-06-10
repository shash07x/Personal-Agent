# config/__init__.py
import json, os
from pathlib import Path

_CONFIG_PATH = Path(__file__).parent / "api_keys.json"

def get_config() -> dict:
    try:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def update_config(**kwargs) -> None:
    cfg = get_config()
    cfg.update(kwargs)
    _CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4)

def get_os() -> str:
    """Returns: 'windows' | 'mac' | 'linux'"""
    return get_config().get("os_system", "windows").lower()

def is_windows() -> bool: return get_os() == "windows"
def is_mac()     -> bool: return get_os() == "mac"
def is_linux()   -> bool: return get_os() == "linux"

def get_voice() -> str:
    return get_config().get("voice_name", "Aoede")

def set_voice(name: str) -> None:
    update_config(voice_name=name)
