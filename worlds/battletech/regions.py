from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import Entrance, Region
if TYPE_CHECKING:
    from .world import BattleTechWorld
from .data.data import data

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

    regions = []
    for region_name in data.regions:
        regions.append(Region(region_name, world.player, world.multiworld))

    # Some regions may only exist if the player enables certain options.
    #if world.options.hammer:
    #    top_middle_room = Region("Top Middle Room", world.player, world.multiworld)
    #    regions.append(top_middle_room)

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions


def connect_regions(world: BattleTechWorld) -> None:
    for i in range(len(data.regions)):
        region_name = data.regions[i]
        next_region_name = data.regions[i+1] if i+1 < len(data.regions) else None
        if next_region_name:
            region = world.get_region(region_name)
            next_region = world.get_region(next_region_name)
            region.connect(next_region, f"{region.name} to {next_region.name}")
