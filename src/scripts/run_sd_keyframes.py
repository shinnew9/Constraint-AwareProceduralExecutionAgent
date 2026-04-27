import argparse

from capea.utils import read_json, log
from capea.visual.sd_generator import StableDiffusionKeyframeGenerator


def main():
    parser = argparse.ArgumentParser(description="Generate Stable Diffusion keyframes from CAPEA prompt JSON.")
    parser.add_argument("--prompts", required=True, help="Path to prompt JSON file")
    parser.add_argument("--model-id", default="runwayml/stable-diffusion-v1-5")
    parser.add_argument("--fallback", action="store_true", help="Use placeholder image generation instead of Stable Diffusion")
    parser.add_argument("--width", type=int, default=768)
    parser.add_argument("--height", type=int, default=512)
    parser.add_argument("--steps", type=int, default=30)
    parser.add_argument("--guidance", type=float, default=7.5)

    args = parser.parse_args()

    data = read_json(args.prompts)

    generator = StableDiffusionKeyframeGenerator(
        model_id=args.model_id,
        use_fallback=args.fallback,
    )

    for item in data["prompts"]:
        log(f"Generating keyframe for {item['node_id']}")

        output_path = generator.generate(
            prompt=item["prompt"],
            negative_prompt=item["negative_prompt"],
            seed=item["seed"],
            output_path=item["output_keyframe"],
            width=args.width,
            height=args.height,
            num_inference_steps=args.steps,
            guidance_scale=args.guidance,
        )

        print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()