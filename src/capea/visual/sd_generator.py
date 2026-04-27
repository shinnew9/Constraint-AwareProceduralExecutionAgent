from pathlib import Path
from typing import Optional

import torch
from PIL import Image, ImageDraw


class StableDiffusionKeyframeGenerator:
    def __init__(
        self,
        model_id: str = "runwayml/stable-diffusion-v1-5",
        device: Optional[str] = None,
        use_fallback: bool = False,
    ):
        self.model_id = model_id
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.use_fallback = use_fallback
        self.pipe = None

        if not self.use_fallback:
            self._load_pipeline()

    def _load_pipeline(self):
        from diffusers import StableDiffusionPipeline

        dtype = torch.float16 if self.device == "cuda" else torch.float32

        self.pipe = StableDiffusionPipeline.from_pretrained(
            self.model_id,
            torch_dtype=dtype,
            safety_checker=None,
            requires_safety_checker=False,
        )
        self.pipe = self.pipe.to(self.device)

        if self.device == "cuda":
            self.pipe.enable_attention_slicing()

    def generate(
        self,
        prompt: str,
        negative_prompt: str,
        seed: int,
        output_path: str | Path,
        width: int = 768,
        height: int = 512,
        num_inference_steps: int = 30,
        guidance_scale: float = 7.5,
    ) -> Path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if self.use_fallback:
            return self._generate_placeholder(prompt, seed, output_path, width, height)

        generator = torch.Generator(device=self.device).manual_seed(seed)

        image = self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=generator,
        ).images[0]

        image.save(output_path)
        return output_path

    def _generate_placeholder(
        self,
        prompt: str,
        seed: int,
        output_path: Path,
        width: int,
        height: int,
    ) -> Path:
        img = Image.new("RGB", (width, height), color=(245, 245, 245))
        draw = ImageDraw.Draw(img)

        text = f"Fallback Keyframe\nSeed: {seed}\n\nPrompt:\n{prompt[:500]}"
        draw.multiline_text((30, 30), text, fill=(0, 0, 0), spacing=8)

        img.save(output_path)
        return output_path