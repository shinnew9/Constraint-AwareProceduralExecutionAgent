import hashlib
import random
from typing import Optional


def stable_seed(key: str, base_seed: int = 42, max_seed: int = 2**31 - 1) -> int:
    raw = f"{base_seed}:{key}".encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    return int(digest[:12], 16) % max_seed


def seed_python(seed: Optional[int] = None) -> int:
    if seed is None:
        seed = 42
    random.seed(seed)
    return seed