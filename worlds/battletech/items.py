from __future__ import annotations
from typing import TYPE_CHECKING
from copy import copy
import math
from BaseClasses import Item, ItemClassification
from .data import constants
from .data.derived_data import weighted_filler_items
from .data.item_data import item_data, BattleTechItemDatum
if TYPE_CHECKING:
    from .world import BattleTechWorld

# Each Item instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Item class and override the "game" field.
class BattleTechItem(Item):
    """Archipelago representation for an item in BattleTech"""
    game = constants.GAME_NAME


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


def get_random_filler_item_name(world: BattleTechWorld) -> str:
    return weighted_filler_items[world.random.randint(0, len(weighted_filler_items)-1)].item_name
    #TODO do random without repeats instead of pure random


def create_item(world: BattleTechWorld, name: str) -> BattleTechItem:
    item: BattleTechItemDatum = next(x for x in item_data if name == x.item_name)
    return BattleTechItem(name, item.item_classification, item.item_id, world.player)


def create_all_items(world: BattleTechWorld) -> None:
    item_pool: list[Item] = []
    for item in item_data:
        bt_item = BattleTechItem(item.item_name, item.item_classification, item.item_id, world.player)
        if item.item_id < 100: # Progressive tonnages
            tonnage_item_count = get_tonnage_item_count(item, world)
            for _ in range(tonnage_item_count):
                item_pool.append(copy(bt_item))
        elif constants.FIRST_ABILITY_OPTION_ITEM_ID <= item.item_id and \
                item.item_id < constants.LAST_ABILITY_OPTION_ITEM_ID:
            # TODO pull from options instead of defaults
            if item.default_option_value == 0:
                item_pool.append(bt_item)
            else:
                world.push_precollected(bt_item)
        elif item.count is not None:
            for _ in range(item.count):
                item_pool.append(copy(bt_item))
        elif item.item_classification == ItemClassification.filler:
            pass # Handled by create_filler()
        else:
            assert False, f"Item {item} is not filler, has no count, and has no special rules"

    number_of_items = len(item_pool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    assert needed_number_of_filler_items >= 0, f"More items than locations exist"
    item_pool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += item_pool
