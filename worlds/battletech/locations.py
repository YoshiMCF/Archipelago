from __future__ import annotations
from typing import TYPE_CHECKING

from BaseClasses import ItemClassification as IC, Location
from . import items
if TYPE_CHECKING:
    from .world import BattleTechWorld
from .data.data import data
from .data.location_data import BattleTechLocationData, BattleTechStaticLocationDatum, BattleTechStaticLocationType

# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class BattleTechLocation(Location):
    game = "BATTLETECH"


def create_locations(world: BattleTechWorld) -> None:
    last_story_location_datum: BattleTechStaticLocationDatum = next( \
            (x for x in reversed(data.location_data.static_locations) \
            if x.location_type == BattleTechStaticLocationType.story), None)
    assert last_story_location_datum

    for location_datum in data.locations:
        if isinstance(location_datum, BattleTechStaticLocationDatum):
            region = world.get_region(location_datum.region)
            assert region
            if location_datum.location_id == last_story_location_datum.location_id:
                location = BattleTechLocation(world.player, location_datum.location_name, None, region)
                victory_item = items.BattleTechItem("Victory", IC.progression, None, world.player)
                location.place_locked_item(victory_item)
                region.locations.append(location)
            else:
                location_id = None if location_datum == last_story_location_datum else location_datum.location_id
                location = BattleTechLocation(world.player, location_datum.location_name, location_id, region)
                region.locations.append(location)
        else:
            # TODO don't need all 100 dynamic locations per dynamic location
            region = world.get_region(location_datum.region)
            assert region
            location = BattleTechLocation(world.player, location_datum.location_name, location_datum.location_id,
                    region)
            region.locations.append(location)
