from __future__ import annotations
from typing import TYPE_CHECKING

def parse_int(s: str) -> int | None:
    return int(s) if s else None

def parse_float(s: str) -> float | None:
    return float(s) if s else None

def empty_str_to_none(s: str) -> str | None:
    return s if s else None
