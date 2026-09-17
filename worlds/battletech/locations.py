from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import ItemClassification as IC, Location
from .items import BattleTechItem
from .data import constants
from .data.derived_data import locations
from .data.location_data import static_location_data, BattleTechStaticLocationDatum, BattleTechStaticLocationType
if TYPE_CHECKING:
    from .world import BattleTechWorld

# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class BattleTechLocation(Location):
    """Archipelago representation of a location check in BattleTech"""
    game = constants.GAME_NAME


def create_locations(world: BattleTechWorld) -> None:
    last_story_location_datum: BattleTechStaticLocationDatum = next( \
            (x for x in reversed(static_location_data) \
            if x.location_type == BattleTechStaticLocationType.event), None)
    assert last_story_location_datum

    for location_datum in locations:
        if isinstance(location_datum, BattleTechStaticLocationDatum):
            region = world.get_region(location_datum.region)
            assert region

            location_id = None if location_datum.location_type == BattleTechStaticLocationType.event \
                    else location_datum.location_id
            location = BattleTechLocation(world.player, location_datum.location_name, location_id, region)

            if location_datum.location_id == last_story_location_datum.location_id:
                victory_item = BattleTechItem("Victory", IC.progression, None, world.player)
                location.place_locked_item(victory_item)
            elif location_datum.location_type == BattleTechStaticLocationType.event:
                event_item = BattleTechItem(location_datum.location_name, IC.progression, None, world.player)
                location.place_locked_item(event_item)

            region.locations.append(location)
        else:
            # TODO don't need all 100 dynamic locations per dynamic location
            region = world.get_region(location_datum.region)
            assert region
            location = BattleTechLocation(world.player, location_datum.location_name, location_datum.location_id,
                    region)
            region.locations.append(location)
