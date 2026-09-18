"""Run object detection with a pretrained Ultralytics YOLO model.

Examples:
    python detect.py --source image.jpg
    python detect.py --source video.mp4 --output results
    python detect.py --source 0
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Union

from ultralytics import YOLO


Source = Union[str, int]


def parse_source(value: str) -> Source:
    """Treat a numeric source as a webcam index, otherwise as a file path."""
    return int(value) if value.isdigit() else value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Detect common objects using a pretrained YOLO model."
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Image/video path or webcam index (for example: image.jpg, video.mp4, or 0).",
    )
    parser.add_argument(
        "--model",
        default="yolo11n.pt",
        help="Ultralytics model name or local .pt path (default: yolo11n.pt).",
    )
    parser.add_argument(
        "--output",
        default="runs",
        help="Folder where annotated images/videos are saved (default: runs).",
    )
    parser.add_argument(
        "--confidence",
        type=float,
        default=0.25,
        help="Minimum confidence from 0 to 1 (default: 0.25).",
    )
    parser.add_argument(
        "--no-view",
        action="store_true",
        help="Save results without opening a preview window.",
    )
    return parser


def validate_args(args: argparse.Namespace) -> None:
    if not 0 <= args.confidence <= 1:
        raise ValueError("--confidence must be between 0 and 1.")
    if isinstance(args.source, str) and not Path(args.source).exists():
        raise FileNotFoundError(f"Source file was not found: {args.source}")


def main() -> None:
    args = build_parser().parse_args()
    args.source = parse_source(args.source)
    validate_args(args)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Ultralytics downloads the selected pretrained model automatically on first use.
    model = YOLO(args.model)
    results = model.predict(
        source=args.source,
        conf=args.confidence,
        project=str(output_dir),
        name="detections",
        exist_ok=True,
        save=True,
        show=not args.no_view,
        stream=True,
    )

    for result in results:
        detected = result.boxes is not None and len(result.boxes) > 0
        if detected:
            print(f"Detected {len(result.boxes)} object(s) in {result.path}")
        else:
            print(f"No objects detected in {result.path}")

    print(f"Annotated results saved to: {output_dir / 'detections'}")


if __name__ == "__main__":
    main()
