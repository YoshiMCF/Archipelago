from __future__ import annotations
from . import constants

def parse_int(s: str) -> int | None:
    return int(s) if s else None


def parse_float(s: str) -> float | None:
    return float(s) if s else None


def empty_str_to_none(s: str) -> str | None:
    return s if s else None


# SimGameBattleSimulator.GetLanceTonnageRating()
def lance_tonnage_to_bracket(lance_tonnage: int) -> int:
    for i, tonnage in enumerate(constants.LANCE_DROP_TONNAGE_BRACKETS):
        if lance_tonnage >= tonnage:
            return i+1
    return 0


def min_tonnage_for_difficulty_level(difficulty_level: int) -> int:
    if difficulty_level == 0:
        return 0
    return constants.LANCE_DROP_TONNAGE_BRACKETS[difficulty_level - 1]
