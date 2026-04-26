import sys
from pathlib import Path

from PIL import Image, ImageDraw

from capea.utils import read_json, ensure_dir


def make_placeholder_image(prompt_item: dict, output_path: Path):
    img = Image.new("RGB", (768, 512), color=(245, 245, 245))
    draw = ImageDraw.Draw(img)

    text = (
        f"Node: {prompt_item['node_id']}\n"
        f"Action: {prompt_item['action']} {prompt_item['target']}\n"
        f"Seed: {prompt_item['seed']}\n\n"
        f"Prompt:\n{prompt_item['prompt'][:250]}"
    )

    draw.multiline_text((30, 30), text, fill=(0, 0, 0), spacing=8)
    img.save(output_path)


def main():
    if len(sys.argv) < 2:
        print("Usage: python src/scripts/run_keyframe_demo.py <prompt_json>")
        sys.exit(1)

    prompt_path = sys.argv[1]
    data = read_json(prompt_path)

    output_dir = ensure_dir("outputs_json/keyframes")

    for item in data["prompts"]:
        output_path = output_dir / f"{item['node_id']}.png"
        make_placeholder_image(item, output_path)
        print(f"Saved keyframe: {output_path}")


if __name__ == "__main__":
    main()