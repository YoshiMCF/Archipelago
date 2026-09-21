from __future__ import annotations
from typing import TYPE_CHECKING
import math
from rule_builder.rules import Has, HasFromList, And, Rule
from .data.item_data import item_data
from .data.derived_data import ability_items
from .data.location_data import static_location_data, BattleTechStaticLocationType
from .data.region_data import region_data
from .data import constants
from .data.utils import min_tonnage_for_difficulty_level
from .regions import get_entrance_name
if TYPE_CHECKING:
    from .world import BattleTechWorld


def set_all_rules(world: BattleTechWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: BattleTechWorld) -> None:
    for i, from_region in enumerate(region_data):
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


def difficulty_to_lance_tonnage_rule(difficulty: int, world: BattleTechWorld) -> Rule:
    required_tonnage = min_tonnage_for_difficulty_level(difficulty)
    start = world.options.lance_starting_tonnage.value
    increment = float(constants.LANCE_TONNAGE_INCREMENT)
    item_count = math.ceil((required_tonnage - start) / increment)
    item_count = max(item_count, 0)

    lance_tonnage_item = next((x for x in item_data if x.item_id == constants.LANCE_TONNAGE_ITEM_ID), None)
    assert lance_tonnage_item
    lance_tonnage_rule = Has(lance_tonnage_item.item_name, count=item_count)
    return lance_tonnage_rule


def difficulty_to_mech_slot_tonnage_rule(difficulty: int, world: BattleTechWorld) -> Rule:
    required_tonnage = min_tonnage_for_difficulty_level(difficulty)
    start = world.options.mech_slot_1_starting_tonnage.value + \
            world.options.mech_slot_2_starting_tonnage.value + \
            world.options.mech_slot_3_starting_tonnage.value + \
            world.options.mech_slot_4_starting_tonnage.value
    increment = float(constants.MECH_SLOT_TONNAGE_INCREMENT)
    item_count = math.ceil((required_tonnage - start) / increment)
    item_count = max(item_count, 0)

    mech_tonnage_item_names: list[str] = []
    for item_id in constants.MECH_SLOT_TONNAGE_ITEM_IDS:
        item = next((x for x in item_data if x.item_id == item_id), None)
        assert item
        mech_tonnage_item_names.append(item.item_name)
    mech_tonnage_rule = HasFromList(*mech_tonnage_item_names, count=item_count)
    return mech_tonnage_rule


def difficulty_to_rule(difficulty: int, world: BattleTechWorld) -> Rule:
    return difficulty_to_lance_tonnage_rule(difficulty, world) & difficulty_to_mech_slot_tonnage_rule(difficulty, world)


def get_ability_requirement_rule(mission_index: int) -> Rule:
    ability_item_names: list[str] = []
    ability_item_count = mission_index + 1
    for ability_item_list in ability_items:
        ability_item_names.extend(map(lambda x: x.item_name, ability_item_list))
        if len(ability_item_names) >= ability_item_count:
            break
    ability_item_count = min(ability_item_count, len(ability_item_names))
    return HasFromList(*ability_item_names, count=ability_item_count)


def set_all_location_rules(world: BattleTechWorld) -> None:
    story_index = 0
    event_index = 0
    for location_datum in static_location_data:
        location = world.get_location(location_datum.location_name)

        ability_rule: Rule | None = None
        match location_datum.location_type:
            case BattleTechStaticLocationType.STORY:
                ability_rule = get_ability_requirement_rule(story_index)
                story_index += 1
            case BattleTechStaticLocationType.EVENT:
                ability_rule = get_ability_requirement_rule(event_index)
                event_index += 1

        difficulty_rule: Rule | None = None
        if location_datum.difficulty:
            difficulty_rule = difficulty_to_rule(location_datum.difficulty, world)

        if ability_rule is not None and difficulty_rule is not None:
            world.set_rule(location, And(ability_rule, difficulty_rule))
        elif ability_rule is not None:
            world.set_rule(location, ability_rule)
        elif difficulty_rule is not None:
            world.set_rule(location, difficulty_rule)


def set_completion_condition(world: BattleTechWorld) -> None:
    world.set_completion_rule(Has(constants.VICTORY_ITEM))


# One final comment about rules:
# If your world exclusively uses Rule Builder rules (like APQuest), it's worth trying CachedRuleBuilderWorld.
# CachedRuleBuilderWorld is a subclass of World that has a bunch of caching magic to make rules faster.
# Just have your world class subclass CachedRuleBuilderWorld instead of World:
#   class APQuestWorld(CachedRuleBuilderWorld): ...
# This may speed up your world, or it may make it slower.
# The exact factors are complex and not well understood, but there is no harm in trying it.
# Generate a few seeds and see if there is a noticeable difference!
# If you're wondering, author has checked: APQuest is too simple to see any benefits, so we'll stick with "World".
