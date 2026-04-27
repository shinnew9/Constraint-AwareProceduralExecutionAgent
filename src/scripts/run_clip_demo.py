import argparse
from pathlib import Path

from capea.utils import read_json, log
from capea.visual.clip_generator import KeyframeClipGenerator


def main():
    parser = argparse.ArgumentParser(description="Generate short MP4 clips from CAPEA keyframes.")
    parser.add_argument("--prompts", required=True, help="Path to prompt JSON file")
    parser.add_argument("--fps", type=int, default=8)
    parser.add_argument("--duration", type=float, default=2.0)
    parser.add_argument("--no-label", action="store_true")

    args = parser.parse_args()

    data = read_json(args.prompts)

    generator = KeyframeClipGenerator(
        fps=args.fps,
        duration_seconds=args.duration,
    )

    for item in data["prompts"]:
        keyframe_path = Path(item["output_keyframe"])
        clip_path = Path(item["output_clip"])

        label = None
        if not args.no_label:
            label = f"{item['node_id']} | {item['action']} {item['target']}"

        log(f"Generating clip for {item['node_id']}")
        output_path = generator.generate_clip(
            image_path=keyframe_path,
            output_path=clip_path,
            label=label,
        )

        print(f"Saved clip: {output_path}")


if __name__ == "__main__":
    main()