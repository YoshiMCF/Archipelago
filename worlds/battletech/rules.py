from __future__ import annotations
from typing import TYPE_CHECKING
import math
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, HasFromList, Rule
if TYPE_CHECKING:
    from .world import BattleTechWorld
from .data.item_data import item_data
from .data.location_data import static_location_data
from .data.derived_data import locations
from .data.region_data import region_data, BattleTechRegionDatum
from .data import constants
from .data.utils import min_tonnage_for_difficulty_level
from .regions import get_entrance_name

HAS_KEY = Has("Key")  # Hmm, what could this be? A little foreshadowing perhaps? :) You'll find out if you keep reading!


def set_all_rules(world: BattleTechWorld) -> None:
    # In order for AP to generate an item layout that is actually possible for the player to complete,
    # we need to define rules for our Entrances and Locations.
    # Note: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.

    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: BattleTechWorld) -> None:
    for i in range(len(region_data)):
        from_region = region_data[i]
        to_region = region_data[i+1] if i+1 < len(region_data) else None
        if to_region:
            entrance = world.get_entrance(get_entrance_name(from_region, to_region))

            found_unlock = False
            for location in static_location_data:
                if location.unlocks_region == to_region.region_name:
                    world.set_rule(entrance, Has(location.location_name))
                    found_unlock = True
                    break
            assert found_unlock

    # So far, we've been using "Has" from the Rule Builder to make our rules.
    # There is another way to make rules that you will see in a lot of older worlds.
    # A rule can just be a function that takes a "state" argument and returns a bool.
    # As a demonstration of what that looks like, let's do it with our final Entrance rule:
    #world.set_rule(overworld_to_top_left_room, lambda state: state.has("Key", world.player))

    # Rule Builder is quite comprehensive, and even if you have really esoteric rules,
    # you can make custom rules by subclassing CustomRule.

def difficulty_to_lance_tonnage_rule(difficulty: int, world: BattleTechWorld) -> Rule:
    required_tonnage = min_tonnage_for_difficulty_level(difficulty)
    start = world.options.min_lance_tonnage
    increment = float(world.options.lance_tonnage_increment)
    item_count = math.ceil((required_tonnage - start) / increment)
    item_count = max(item_count, 0)

    lance_tonnage_item = next((x for x in item_data if (x.item_id == constants.LANCE_TONNAGE_ITEM_ID)), None)
    assert lance_tonnage_item
    lance_tonnage_rule = Has(lance_tonnage_item.item_name, count=item_count)
    return lance_tonnage_rule


def difficulty_to_mech_slot_tonnage_rule(difficulty: int, world: BattleTechWorld) -> Rule:
    required_tonnage = min_tonnage_for_difficulty_level(difficulty)
    start = world.options.min_mech_slot_1_tonnage + \
            world.options.min_mech_slot_2_tonnage + \
            world.options.min_mech_slot_3_tonnage + \
            world.options.min_mech_slot_4_tonnage
    #TODO either make this a constant or 1 value for all slots
    increment = float(world.options.mech_slot_1_tonnage_increment)
    item_count = math.ceil((required_tonnage - start) / increment)
    item_count = max(item_count, 0)

    mech_tonnage_item_names: list[BattleTechItemDatum] = []
    for item_id in constants.MECH_SLOT_TONNAGE_ITEM_IDS:
        item = next((x for x in item_data if (x.item_id == item_id)), None)
        assert item
        mech_tonnage_item_names.append(item.item_name)
    mech_tonnage_rule = HasFromList(*mech_tonnage_item_names, count=item_count)
    return mech_tonnage_rule


def difficulty_to_rule(difficulty: int, world: BattleTechWorld) -> Rule:
    return difficulty_to_lance_tonnage_rule(difficulty, world) & difficulty_to_mech_slot_tonnage_rule(difficulty, world)


def set_all_location_rules(world: BattleTechWorld) -> None:
    for location_datum in static_location_data:
        if location_datum.difficulty:
            location = world.get_location(location_datum.location_name)
            world.set_rule(location, difficulty_to_rule(location_datum.difficulty, world))


def set_completion_condition(world: BattleTechWorld) -> None:
    world.set_completion_rule(Has("Victory"))


# One final comment about rules:
# If your world exclusively uses Rule Builder rules (like APQuest), it's worth trying CachedRuleBuilderWorld.
# CachedRuleBuilderWorld is a subclass of World that has a bunch of caching magic to make rules faster.
# Just have your world class subclass CachedRuleBuilderWorld instead of World:
#   class APQuestWorld(CachedRuleBuilderWorld): ...
# This may speed up your world, or it may make it slower.
# The exact factors are complex and not well understood, but there is no harm in trying it.
# Generate a few seeds and see if there is a noticeable difference!
# If you're wondering, author has checked: APQuest is too simple to see any benefits, so we'll stick with "World".
