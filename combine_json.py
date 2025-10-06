"""Combine all JSON files in a directory into a single `all.json` file.

Usage:
    python combine_json.py
    python combine_json.py --directory /path/to/jsons --output merged.json

The script expects each JSON file to contain either a JSON array or an object.
Objects are wrapped in a list before being added to the combined output.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable, List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Combine all JSON files in a directory into a single JSON file. "
            "JSON arrays are concatenated; JSON objects are wrapped in a list."
        )
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=Path,
        default=Path.cwd(),
        help="Directory containing JSON files (default: current working directory)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("all.json"),
        help="Output JSON file name (default: all.json)",
    )
    return parser.parse_args()


def collect_json_files(directory: Path, output_path: Path) -> List[Path]:
    json_files = sorted(directory.glob("*.json"))
    return [path for path in json_files if path.resolve() != output_path.resolve()]


def load_json_as_list(path: Path) -> List[object]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Failed to parse {path}") from exc

    if isinstance(data, list):
        return data

    return [data]


def write_combined_json(output_path: Path, entries: Iterable[object]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(list(entries), handle, ensure_ascii=False, indent=2)


def main() -> None:
    args = parse_args()
    directory = args.directory.resolve()
    output_path = args.output if args.output.is_absolute() else directory / args.output

    if not directory.is_dir():
        raise NotADirectoryError(f"Directory does not exist: {directory}")

    json_files = collect_json_files(directory, output_path)

    combined: List[object] = []
    for json_file in json_files:
        combined.extend(load_json_as_list(json_file))

    write_combined_json(output_path, combined)

    print(f"Combined {len(json_files)} file(s) into {output_path} with {len(combined)} item(s).")


if __name__ == "__main__":
    main()
