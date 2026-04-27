from pathlib import Path
from typing import List

import imageio.v2 as imageio


class VideoStitcher:
    def __init__(self, fps: int = 8):
        self.fps = fps

    def stitch(
        self,
        clip_paths: List[str | Path],
        output_path: str | Path,
    ) -> Path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        all_frames = []

        for clip_path in clip_paths:
            clip_path = Path(clip_path)

            if not clip_path.exists():
                raise FileNotFoundError(f"Clip not found: {clip_path}")

            reader = imageio.get_reader(str(clip_path))

            for frame in reader:
                all_frames.append(frame)

            reader.close()

        imageio.mimsave(
            output_path,
            all_frames,
            fps=self.fps,
            codec="libx264",
            quality=8,
            macro_block_size=16,
        )

        return output_path