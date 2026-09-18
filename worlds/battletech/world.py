from collections.abc import Mapping
from typing import Any
from worlds.AutoWorld import World
from . import items, locations, regions, rules, web_world
from .options import BattleTechOptions
from .data import constants
from .data.derived_data import location_names_to_ids, item_names_to_ids

# The world class is the heart and soul of an apworld implementation.
# It holds all the data and functions required to build the world and submit it to the multiworld generator.
# You could have all your world code in just this one class, but for readability and better structure,
# it is common to split up world functionality into multiple files.
# This implementation in particular has the following additional files, each covering one topic:
# regions.py, locations.py, rules.py, items.py, options.py and web_world.py.
# It is recommended that you read these in that specific order, then come back to the world class.
class BattleTechWorld(World):
    """
	Take command of your own mercenary outfit of 'Mechs and the MechWarriors that pilot them,
	struggling to stay afloat as you find yourself drawn into a brutal interstellar civil war.
    """

    game = constants.GAME_NAME

    web = web_world.BattleTechWebWorld()

    options_dataclass = BattleTechOptions
    options: BattleTechOptions

    location_name_to_id = location_names_to_ids
    item_name_to_id = item_names_to_ids
    origin_region_name = constants.STARTING_REGION

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.BattleTechItem:
        return items.create_item(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict(
                "mech_slot_1_starting_tonnage",
                "mech_slot_2_starting_tonnage",
                "mech_slot_3_starting_tonnage",
                "mech_slot_4_starting_tonnage",
                "lance_starting_tonnage",
                "auto_scout_argo_locations",
                "auto_scout_salvage_locations",
                "ap_salvage_drop_chance",
                "cash_reward_amount",
                "pilot_xp_reward_amount",
                "morale_reward_amount",
                "high_spirits_reward_duration",
                "tech_points_reward_amount",
                "med_points_reward_amount",
                "xp_per_day_reward_amount",
                "xp_cap_reward_amount",
                "argo_drive_speed_multiplier"
        )
