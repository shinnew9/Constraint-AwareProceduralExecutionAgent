import re


def normalize_id(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text


def make_resource_id(name: str, index: int = 1) -> str:
    return f"{normalize_id(name)}_{index}"


def make_node_id(action: str, target: str, index: int = 1) -> str:
    return f"{normalize_id(action)}_{normalize_id(target)}_{index}"