#!/usr/bin/env python3
"""Extract contract details from `x.html` into JSON."""

from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List

FIELD_ID_MAP = {
    "contract_id": "Repeater1_lblCustomerId_{idx}",
    "contract_description": "Repeater1_lblContactName_{idx}",
    "contractor": "Repeater1_lblCountry_{idx}",
    "implementing_office": "Repeater1_Label5_{idx}",
    "source_of_funds": "Repeater1_Label6_{idx}",
    "contract_cost_php": "Repeater1_Label2_{idx}",
    "contract_effectivity_date": "Repeater1_Label3_{idx}",
    "contract_expiry_date": "Repeater1_Label4_{idx}",
    "status": "Repeater1_Label7_{idx}",
    "percent_accomplishment": "Repeater1_Label1_{idx}",
}

INDEX_PATTERN = re.compile(r"Repeater1_[^_]+_(\d+)$")


class ContractHTMLParser(HTMLParser):
    """HTML parser that captures text content keyed by their element ids."""

    def __init__(self) -> None:
        super().__init__()
        self._current_id: str | None = None
        self.values: Dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs):  # type: ignore[override]
        if tag.lower() != "span":
            return
        attr_dict = dict(attrs)
        element_id = attr_dict.get("id")
        if element_id:
            self._current_id = element_id
            self.values.setdefault(element_id, "")

    def handle_data(self, data: str) -> None:  # type: ignore[override]
        if not self._current_id:
            return
        text = data.strip()
        if not text:
            return
        if self.values[self._current_id]:
            self.values[self._current_id] += f" {text}"
        else:
            self.values[self._current_id] = text

    def handle_endtag(self, tag: str) -> None:  # type: ignore[override]
        if tag.lower() == "span":
            self._current_id = None


def parse_contracts(html_source: str) -> List[Dict[str, str | None]]:
    parser = ContractHTMLParser()
    parser.feed(html_source)
    raw_values = parser.values

    indices = sorted(
        {int(match.group(1)) for element_id in raw_values if (match := INDEX_PATTERN.match(element_id))}
    )

    contracts: List[Dict[str, str | None]] = []
    for idx in indices:
        record: Dict[str, str | None] = {}
        for field, id_template in FIELD_ID_MAP.items():
            element_id = id_template.format(idx=idx)
            value = raw_values.get(element_id)
            record[field] = value if value is not None else None
        # Skip rows without a contract id.
        if record.get("contract_id"):
            contracts.append(record)

    return contracts


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract contract details from an HTML file into JSON.")
    parser.add_argument(
        "html_path",
        nargs="?",
        default="x.html",
        help="Path to the source HTML file (default: x.html)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output filename to write JSON data (stdout if omitted)",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="Indentation level for JSON output (default: 2)",
    )
    args = parser.parse_args()

    html_file = Path(args.html_path)
    if not html_file.is_file():
        raise FileNotFoundError(f"HTML file not found: {html_file}")

    html_source = html_file.read_text(encoding="utf-8")
    contracts = parse_contracts(html_source)
    contract_count = len(contracts)

    json_payload = json.dumps(contracts, ensure_ascii=False, indent=args.indent)

    if args.output:
        output_path = Path(args.output)
        suffix = "".join(output_path.suffixes)
        base_name = output_path.name[: -len(suffix)] if suffix else output_path.name
        new_name = f"{base_name}_{contract_count}{suffix}"
        final_path = output_path.with_name(new_name)
        final_path.write_text(json_payload + "\n", encoding="utf-8")
    else:
        print(json_payload)


if __name__ == "__main__":
    main()
