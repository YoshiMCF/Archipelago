from __future__ import annotations
import math
from . import constants
from .item_data import BattleTechItemDatum
from ..world import BattleTechWorld

def parse_int(s: str) -> int | None:
    return int(s) if s else None


def parse_float(s: str) -> float | None:
    return float(s) if s else None


def empty_str_to_none(s: str) -> str | None:
    return s if s else None


# SimGameBattleSimulator.GetLanceTonnageRating()
def lance_tonnage_to_bracket(lance_tonnage: int) -> int:
    for i in range(len(constants.LANCE_DROP_TONNAGE_BRACKETS)):
        if lance_tonnage >= constants.LANCE_DROP_TONNAGE_BRACKETS[i]:
            return i+1
    return 0


def min_tonnage_for_difficulty_level(difficulty_level: int) -> int:
    if difficulty_level == 0:
        return 0
    return constants.LANCE_DROP_TONNAGE_BRACKETS[difficulty_level - 1]


def get_tonnage_item_count(item: BattleTechItemDatum, world: BattleTechWorld) -> int:
    starting_value = 0
    increment = 0
    ending_value = 0
    if item.item_id == constants.MECH_SLOT_TONNAGE_ITEM_IDS[0]:
        starting_value = world.options.mech_slot_1_starting_tonnage.value
        increment = constants.MECH_SLOT_TONNAGE_INCREMENT
        ending_value = constants.MAX_MECH_TONNAGE
    elif item.item_id == constants.MECH_SLOT_TONNAGE_ITEM_IDS[1]:
        starting_value = world.options.mech_slot_2_starting_tonnage.value
        increment = constants.MECH_SLOT_TONNAGE_INCREMENT
        ending_value = constants.MAX_MECH_TONNAGE
    elif item.item_id == constants.MECH_SLOT_TONNAGE_ITEM_IDS[2]:
        starting_value = world.options.mech_slot_3_starting_tonnage.value
        increment = constants.MECH_SLOT_TONNAGE_INCREMENT
        ending_value = constants.MAX_MECH_TONNAGE
    elif item.item_id == constants.MECH_SLOT_TONNAGE_ITEM_IDS[3]:
        starting_value = world.options.mech_slot_4_starting_tonnage.value
        increment = constants.MECH_SLOT_TONNAGE_INCREMENT
        ending_value = constants.MAX_MECH_TONNAGE
    elif item.item_id == constants.LANCE_TONNAGE_ITEM_ID:
        starting_value = world.options.lance_starting_tonnage.value
        increment = constants.LANCE_TONNAGE_INCREMENT
        ending_value = constants.MAX_LANCE_TONNAGE
    else:
        assert False, f"Unknown tonnage item {item}"
    result = math.ceil((ending_value - starting_value) / increment)
    assert result >= 0, f"Item {item} must have starting value >= {ending_value}"
    return result
