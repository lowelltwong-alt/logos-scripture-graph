"""Command-line boundary for portable OCR."""

from __future__ import annotations

import argparse
from pathlib import Path

from .contracts import load_json
from .engines import build_engine
from .handoff import build_handoff
from .pipeline import run_pipeline
from .review import build_review


def main() -> None:
    parser = argparse.ArgumentParser(prog="portable-ocr")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run")
    run.add_argument("--source", type=Path, required=True)
    run.add_argument("--config", type=Path, required=True)
    run.add_argument("--output-root", type=Path, required=True)
    review = commands.add_parser("build-review")
    review.add_argument("--run-dir", type=Path, required=True)
    review.add_argument("--output", type=Path, required=True)
    review.add_argument("--confidential-mode", action="store_true")
    handoff = commands.add_parser("build-handoff")
    handoff.add_argument("--run-dir", type=Path, required=True)
    handoff.add_argument("--review", type=Path, required=True)
    handoff.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "run":
        config = load_json(args.config)
        print(run_pipeline(args.source, args.output_root,
                           [build_engine(row) for row in config.get("engines", [])], config.get("policy", {})))
    elif args.command == "build-review":
        print(build_review(args.run_dir, args.output, confidential_mode=args.confidential_mode))
    else:
        print(build_handoff(args.run_dir, args.review, args.output))


if __name__ == "__main__":
    main()
