from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


def nested(payload: dict[str, Any], *keys: str, default: Any = None) -> Any:
    value: Any = payload
    for key in keys:
        if not isinstance(value, dict) or key not in value:
            return default
        value = value[key]
    return value


def captured_at(payload: dict[str, Any]) -> datetime:
    raw = payload.get("captured_at") or payload.get("timestamp")
    if isinstance(raw, str):
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    return datetime.now(UTC)


def object_dict(value: object) -> dict[str, object]:
    """Return a string-keyed mapping for an untrusted nested payload value."""
    if not isinstance(value, dict):
        return {}
    return {key: item for key, item in value.items() if isinstance(key, str)}


def string_list(value: object) -> list[str]:
    """Normalize a JSON array to strings without treating scalar strings as arrays."""
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def optional_float(value: object) -> float | None:
    if isinstance(value, (int, float, str)) and not isinstance(value, bool):
        return float(value)
    return None


def optional_int(value: object) -> int | None:
    if isinstance(value, (int, str)) and not isinstance(value, bool):
        return int(value)
    return None
