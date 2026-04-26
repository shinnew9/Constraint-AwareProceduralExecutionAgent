from dataclasses import dataclass


@dataclass
class CAPEAConfig:
    base_seed: int = 42
    max_parallel_tasks: int = 3
    allow_replanning: bool = True
    default_task_duration: int = 1
    clip_similarity_threshold: float = 0.28
    output_dir: str = "outputs"


DEFAULT_CONFIG = CAPEAConfig()