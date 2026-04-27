import argparse
from pathlib import Path

from capea.utils import read_json, log, ensure_dir
from capea.visual.video_stitcher import VideoStitcher


def main():
    parser = argparse.ArgumentParser(description="Stitch CAPEA video clips into one final procedural video.")
    parser.add_argument("--prompts", required=True, help="Path to prompt JSON file")
    parser.add_argument("--output", default=None, help="Output final MP4 path")
    parser.add_argument("--fps", type=int, default=8)

    args = parser.parse_args()

    data = read_json(args.prompts)

    clip_paths = [item["output_clip"] for item in data["prompts"]]

    if args.output is None:
        source_name = Path(data.get("source", "final")).stem
        output_dir = ensure_dir("outputs_json/final")
        output_path = output_dir / f"{source_name}_final.mp4"
    else:
        output_path = Path(args.output)

    log("Stitching clips into final video")
    stitcher = VideoStitcher(fps=args.fps)
    final_path = stitcher.stitch(clip_paths, output_path)

    print(f"\nSaved final video: {final_path}")


if __name__ == "__main__":
    main()