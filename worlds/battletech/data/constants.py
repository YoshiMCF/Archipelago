from __future__ import annotations
from typing import TYPE_CHECKING
import enum

MAX_MECH_TONNAGE = 100
MECHS_PER_LANCE = 4
MAX_LANCE_TONNAGE = MAX_MECH_TONNAGE * MECHS_PER_LANCE

DIFFICULTY_LEVELS = 10

# BattleTech_Data/StreamingAssets/data/simGameConstants/SimGameConstants.json
LANCE_DROP_TONNAGE_BRACKETS = [100, 125, 150, 175, 200, 225, 250, 275, 300, 325]

# SimGameBattleSimulator.GetLanceTonnageRating()
def lance_tonnage_to_bracket(lance_tonnage: int) -> int:
    for i in range(len(LANCE_DROP_TONNAGE_BRACKETS)):
        if lance_tonnage >= LANCE_DROP_TONNAGE_BRACKETS:
            return i+1
    return 0

def min_tonnage_for_difficulty_level(difficulty_level: int) -> int:
    if difficulty_level == 0:
        return 0
    return LANCE_DROP_TONNAGE_BRACKETS[difficulty_level - 1]
