from pathlib import Path
from typing import Optional

import imageio.v2 as imageio
from PIL import Image, ImageDraw


class KeyframeClipGenerator:
    def __init__(self, fps: int = 8, duration_seconds: float = 2.0):
        self.fps = fps
        self.duration_seconds = duration_seconds

    def generate_clip(
        self,
        image_path: str | Path,
        output_path: str | Path,
        label: Optional[str] = None,
    ) -> Path:
        image_path = Path(image_path)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if not image_path.exists():
            raise FileNotFoundError(f"Keyframe image not found: {image_path}")

        image = Image.open(image_path).convert("RGB")
        frame_count = int(self.fps * self.duration_seconds)

        frames = []
        for i in range(frame_count):
            frame = image.copy()

            # simple subtle zoom effect
            scale = 1.0 + 0.02 * (i / max(frame_count - 1, 1))
            frame = self._center_zoom(frame, scale)

            if label:
                frame = self._draw_label(frame, label)

            frames.append(frame)

        imageio.mimsave(
            output_path,
            frames,
            fps=self.fps,
            codec="libx264",
            quality=8,
            macro_block_size=16,
        )

        return output_path

    def _center_zoom(self, image: Image.Image, scale: float) -> Image.Image:
        w, h = image.size

        new_w = int(w / scale)
        new_h = int(h / scale)

        left = (w - new_w) // 2
        top = (h - new_h) // 2
        right = left + new_w
        bottom = top + new_h

        cropped = image.crop((left, top, right, bottom))
        return cropped.resize((w, h), Image.Resampling.LANCZOS)

    def _draw_label(self, image: Image.Image, label: str) -> Image.Image:
        draw = ImageDraw.Draw(image)
        draw.rectangle((10, 10, 520, 52), fill=(0, 0, 0))
        draw.text((20, 22), label, fill=(255, 255, 255))
        return image