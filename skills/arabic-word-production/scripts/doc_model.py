from __future__ import annotations

import json
from pathlib import Path


SUPPORTED_BLOCKS = {
    "heading",
    "paragraph",
    "list",
    "table",
    "image",
    "callout",
    "page_break",
}


def validate_model(model: dict) -> dict:
    if not isinstance(model, dict):
        raise ValueError("Document model must be a JSON object")
    if not isinstance(model.get("title", ""), str):
        raise ValueError("title must be a string")
    blocks = model.get("blocks", [])
    if not isinstance(blocks, list):
        raise ValueError("blocks must be an array")
    for index, block in enumerate(blocks):
        if not isinstance(block, dict):
            raise ValueError(f"Block {index} must be an object")
        block_type = block.get("type")
        if block_type not in SUPPORTED_BLOCKS:
            raise ValueError(f"Unsupported block type at index {index}: {block_type}")
        if block_type in {"heading", "paragraph", "callout"} and not isinstance(block.get("text"), str):
            raise ValueError(f"Block {index} requires string field 'text'")
        if block_type == "list" and not isinstance(block.get("items"), list):
            raise ValueError(f"Block {index} requires array field 'items'")
        if block_type == "table":
            if not isinstance(block.get("headers"), list) or not isinstance(block.get("rows"), list):
                raise ValueError(f"Block {index} requires arrays 'headers' and 'rows'")
        if block_type == "image" and not isinstance(block.get("path"), str):
            raise ValueError(f"Block {index} requires string field 'path'")
    return model


def load_model(path: str | Path) -> dict:
    source = Path(path)
    try:
        model = json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {source}: {error}") from error
    return validate_model(model)


__all__ = ["load_model", "validate_model", "SUPPORTED_BLOCKS"]
