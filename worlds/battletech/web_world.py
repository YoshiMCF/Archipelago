from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld
from .data import constants
from .options import option_groups, option_presets

class BattleTechWebWorld(WebWorld):
    """Display data for BattleTech on the website"""
    # pylint: disable=too-few-public-methods
    game = constants.GAME_NAME

    # You can choose between dirt, grass, grassFlowers, ice, jungle, ocean, partyTime, and stone.
    theme = "grassFlowers"

    setup_en = Tutorial(
        # Title
        "Multiworld Setup Guide",
        # Description
        "A guide to setting up BattleTech for MultiWorld.",
        # Language
        "English",
        # Filepath (relative to docs/)
        "setup_en.md",
        # Link
        "setup/en",
        # Authors
        ["Yoshi MCF"],
    )

    tutorials = [setup_en]

    option_groups = option_groups
    options_presets = option_presets
