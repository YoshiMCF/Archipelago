from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import BattleTechWorld

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
    # TODO move to yaml or json?

#    start = Region("Overworld", world.player, world.multiworld)
    region = lambda name : Region(name, world.player, world.multiworld)

    # Mission 2: Rent to Own, Ur Cruinne
    # Alloway, Bellerophon, Detroit
    # Mission 3: Capture the Argo, Axylus - TODO are these all accessible later?
    start = region("Start")
    # Mission 4: Liberation of Weldry
    weldry = region("Weldry")
    # Mission 5: Liberation: Panzyr
    panzyr = region("Panzyr")
    # Mission 6: Liberation: Smithon
    smithon = region("Smithon")
    # Mission 7: Served Cold, Anvelt
    anvelt = region("Anvelt")
    # Mission 8: Raising the Dead, Artru
    # Mission 9: Escape
    # TODO is this accessible again later? No shop on Artru.
    artru = region("Artru")
    # Mission 10: Defense: Smithon
    # Mission 11: Liberate: Itrom
    itrom = region("Itrom")
    # Mission 12: Defense: Panzyr
    # Mission 13: Gunboat Diplomacy, Guldra
    guldra = region("Guldra")
    # Mission 14: Liberate: Tyrlon
    tyrlon = region("Tyrlon")
    # Mission 15: Locura, Lyris
    lyris = region("Lyris")
    # Mission 16: Showdown, Coromodir
    coromodir = region("Coromodir")

    #TODO see if regions actually exist or if there's just the one
    #regions = [start, weldry, panzyr, smithon, anvelt, artru, itrom, guldra, tyrlon, lyris, coromodir]
    regions = [start]

    # Some regions may only exist if the player enables certain options.
    #if world.options.hammer:
    #    top_middle_room = Region("Top Middle Room", world.player, world.multiworld)
    #    regions.append(top_middle_room)

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions


def connect_regions(world: BattleTechWorld) -> None:
    #TODO connect as they're created? Seems better

    # TODO will this grab other people's regions too?
    for i, region in enumerate(world.multiworld.regions):
        if (i >= len(world.multiworld.regions) - 1):
            continue

        nextRegion: Region = world.multiworld.regions[i+1]
        region.connect(nextRegion, f"{region.name} to {nextRegion.name}")

    # The region.connect helper even allows adding a rule immediately.
    # We'll talk more about rule creation in the set_all_rules() function in rules.py.
    #overworld.connect(top_left_room, "Overworld to Top Left Room", lambda state: state.has("Key", world.player))

    # Some Entrances may only exist if the player enables certain options.
    # In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    # In this case, we previously created an extra "Top Middle Room" region that we now need to connect to Overworld.
    #if world.options.hammer:
    #    top_middle_room = world.get_region("Top Middle Room")
    #    overworld.connect(top_middle_room, "Overworld to Top Middle Room")
