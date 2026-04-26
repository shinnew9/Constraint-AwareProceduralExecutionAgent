from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple


# Minimal cooking ontology. Keep it small first; extend as your experiments grow.
ACTION_RESOURCE_DEFAULTS: Dict[str, str] = {
    "boil": "stove_1",
    "fry": "stove_1",
    "saute": "stove_1",
    "chop": "knife_1",
    "cut": "knife_1",
    "slice": "knife_1",
    "serve": "plate_1",
    "mix": "bowl_1",
}

INVALID_ACTION_TARGETS: set[Tuple[str, str]] = {
    ("boil", "knife"),
    ("chop", "water"),
    ("cut", "water"),
    ("fry", "plate"),
}

STATE_TRANSITIONS: Dict[str, Dict[str, Tuple[str, str]]] = {
    "chop": {"default": ("whole", "chopped")},
    "cut": {"default": ("whole", "cut")},
    "slice": {"default": ("whole", "sliced")},
    "boil": {"water": ("cold", "boiling"), "noodles": ("dry", "cooked")},
    "fry": {"egg": ("raw", "fried")},
}


def infer_resource(action: str, current_resource: str | None = None) -> str:
    if current_resource and current_resource.strip():
        return current_resource
    return ACTION_RESOURCE_DEFAULTS.get(action.lower(), "workspace_1")


def is_semantically_valid(action: str, target: str) -> bool:
    return (action.lower(), target.lower()) not in INVALID_ACTION_TARGETS


def expected_transition(action: str, target: str) -> Tuple[str | None, str | None]:
    rules = STATE_TRANSITIONS.get(action.lower(), {})
    return rules.get(target.lower(), rules.get("default", (None, None)))
