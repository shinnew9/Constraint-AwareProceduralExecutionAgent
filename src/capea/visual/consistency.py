from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict, Any

from capea.utils import stable_seed

seed = stable_seed("onion_1")

class ObjectMemory:
    """Keeps stable visual anchors for objects/resources across generated clips."""

    def __init__(self, path: str = "outputs/object_memory.json", base_seed: int = 42):
        self.path = Path(path)
        self.base_seed = base_seed
        self.memory: Dict[str, Dict[str, Any]] = {}
        if self.path.exists():
            self.memory = json.loads(self.path.read_text())

    def get_anchor(self, object_id: str, description: str = "") -> Dict[str, Any]:
        if object_id not in self.memory:
            seed = self._stable_seed(object_id)
            self.memory[object_id] = {
                "object_id": object_id,
                "seed": seed,
                "description": description,
                "prompt_suffix": f"same {object_id}, consistent color, same shape, same material, stable lighting",
            }
            self.save()
        return self.memory[object_id]

    def prompt_for(self, base_prompt: str, object_ids: list[str]) -> tuple[str, int]:
        anchors = [self.get_anchor(obj) for obj in object_ids]
        suffix = ", ".join(a["prompt_suffix"] for a in anchors)
        seed = anchors[0]["seed"] if anchors else self.base_seed
        return f"{base_prompt}, {suffix}", seed

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.memory, indent=2))

    def _stable_seed(self, key: str) -> int:
        digest = hashlib.md5(f"{self.base_seed}:{key}".encode()).hexdigest()
        return int(digest[:8], 16) % 2_147_483_647
