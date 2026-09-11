from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import Entrance, Region
if TYPE_CHECKING:
    from .world import BattleTechWorld
from .data.region_data import region_data, BattleTechRegionDatum

# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Many games will model their Regions after physical in-game places, but you can also have more abstract regions.
# For a location to be in logic, its containing region must be reachable.
# The Entrances connecting regions can have rules - more on that in rules.py.
# This makes regions especially useful for traversal logic ("Can the player reach this part of the map?")

# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).


def create_and_connect_regions(world: BattleTechWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: BattleTechWorld) -> None:
    # Creating a region is as simple as calling the constructor of the Region class.
    # https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/apworld_dev_faq.md

    regions: list[Region] = []
    for region in region_data:
        regions.append(Region(region.region_name, world.player, world.multiworld))

    # Some regions may only exist if the player enables certain options.
    #if world.options.hammer:
    #    top_middle_room = Region("Top Middle Room", world.player, world.multiworld)
    #    regions.append(top_middle_room)

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions


def get_entrance_name(from_region: BattleTechRegionDatum, to_region: BattleTechRegionDatum) -> str:
    return f"{from_region.region_name} to {to_region.region_name}"


def connect_regions(world: BattleTechWorld) -> None:
    for i in range(len(region_data)):
        from_region = region_data[i]
        to_region = region_data[i+1] if i+1 < len(region_data) else None
        if to_region:
            from_ap_region = world.get_region(from_region.region_name)
            to_ap_region = world.get_region(to_region.region_name)
            from_ap_region.connect(to_ap_region, get_entrance_name(from_region, to_region))
