from dataclasses import dataclass, make_dataclass
import re

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle
from .data.data import data
from .data.item_data import BattleTechItemDatum as BTItem, \
        BattleTechItemOptionType as BTItemOption, \
        BattleTechFindableItemOptionType as BTFindableItemOption

# In this file, we define the options the player can pick.
# The most common types of options are Toggle, Range and Choice.

# Options will be in the game's template yaml.
# They will be represented by checkboxes, sliders etc. on the game's options page on the website.
# (Note: Options can also be made invisible from either of these places by overriding Option.visibility.
#  APQuest doesn't have an example of this, but this can be used for secret / hidden / advanced options.)

# For further reading on options, you can also read the Options API Document:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md



# The first type of Option we'll discuss is the Toggle.
# A toggle is an option that can either be on or off. This will be represented by a checkbox on the website.
# The default for a toggle is "off".
# If you want a toggle to be on by default, you can use the "DefaultOnToggle" class instead of the "Toggle" class.
#class HardMode(Toggle):
#    """
#    In hard mode, the basic enemy and the final boss will have more health.
#    The Health Upgrades become progression, as they are now required to beat the final boss.
#    """

    # The docstring of an option is used as the description on the website and in the template yaml.

    # You'll also want to set a display name, which will determine what the option is called on the website.
#    display_name = "Hard Mode"


#class Hammer(Toggle):
#    """
#    Adds another item to the itempool: The Hammer.
#    The top middle chest will now be locked behind a breakable wall, requiring the Hammer.
#    """
#
#    display_name = "Hammer"


#class ExtraStartingChest(Toggle):
#    """
#    Adds an extra chest in the bottom left, making room for an extra Confetti Cannon.
#    """

#    display_name = "Extra Starting Chest"


#class TrapChance(Range):
#    """
#    Percentage chance that any given Confetti Cannon will be replaced by a Math Trap.
#    """

#    display_name = "Trap Chance"

#    range_start = 0
#    range_end = 100
#    default = 0


#class StartWithOneConfettiCannon(Toggle):
#    """
#    Start with a confetti cannon already in your inventory.
#    Why? Because you deserve it. You get to celebrate yourself without doing any work first.
#    """
#
#    display_name = "Start With One Confetti Cannon"


# A Range is a numeric option with a min and max value. This will be represented by a slider on the website.
#class ConfettiExplosiveness(Range):
#    """
#    How much confetti each use of a confetti cannon will fire.
#    """
#
#    display_name = "Confetti Explosiveness"

#    range_start = 0
#    range_end = 10

#    # Range options must define an explicit default value.
#    default = 3

class APSalvageDropChance(Range):
    """
    Percentage chance of finding an Archipelago item in post-mission salvage.
    Not yet implemented.
    """
    display_name = "Archipelago Salvage Drop Chance"
    range_start = 0
    range_end = 100
    default = 25


# A Choice is an option with multiple discrete choices. This will be represented by a dropdown on the website.
#class PlayerSprite(Choice):
#    """
#    The sprite that the player will have.
#    """

#    display_name = "Player Sprite"

#    option_human = 0
#    option_duck = 1
#    option_horse = 2
#    option_cat = 3

#    # Choice options must define an explicit default value.
#    default = option_human

    # For choices, you can also define aliases.
    # For example, we could make it so "player_sprite: kitty" resolves to "player_sprite: cat" like this:
#    alias_kitty = option_cat


# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class BattleTechStaticOptions(PerGameCommonOptions):
    ap_salvage_drop_chance: APSalvageDropChance
    #hard_mode: HardMode
    #hammer: Hammer
    #extra_starting_chest: ExtraStartingChest
    #start_with_one_confetti_cannon: StartWithOneConfettiCannon
    #trap_chance: TrapChance
    #confetti_explosiveness: ConfettiExplosiveness
    #player_sprite: PlayerSprite


# If we want to group our options by similar type, we can do so as well. This looks nice on the website.
option_groups = [
    #OptionGroup(
    #    "Gameplay Options",
    #    [HardMode, Hammer, ExtraStartingChest, StartWithOneConfettiCannon, TrapChance],
    #),
    #OptionGroup(
    #    "Aesthetic Options",
    #    [ConfettiExplosiveness, PlayerSprite],
    #),
]

# Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
option_presets = {
#    "boring": {
#        "hard_mode": False,
#        "hammer": False,
#        "extra_starting_chest": False,
#        "start_with_one_confetti_cannon": False,
#        "trap_chance": 0,
#        "confetti_explosiveness": ConfettiExplosiveness.range_start,
#        "player_sprite": PlayerSprite.option_human,
#    },
#    "the true way to play": {
#        "hard_mode": True,
#        "hammer": True,
#        "extra_starting_chest": True,
#        "start_with_one_confetti_cannon": True,
#        "trap_chance": 50,
#        "confetti_explosiveness": ConfettiExplosiveness.range_end,
#        "player_sprite": PlayerSprite.option_duck,
#    },
}


class BattleTechOptionsGenerator:
    options = None

    def __init__(self):
        fields = []
        for item in data.items:
            match item.option_type:
                case BTItemOption.progressive:
                    fields.extend(self.make_progressive_classes(item))
                case BTItemOption.random_range:
                    fields.extend(self.make_random_range_classes(item))
                case BTItemOption.optional:
                    fields.extend(self.make_optional_class(item))
                case _:
                    if item.default_value != None:
                        fields.extend(self.make_range_class(item))

        self.options = make_dataclass("BattleTechOptions", fields=fields, bases=(BattleTechStaticOptions,))

    def name_to_py(self, name: str) -> str:
        result = name.lower()
        result = result.replace(" ", "_")
        result = re.sub(r"\W", "", result) # remove [^a-zA-Z0-9_]
        return result

    def make_progressive_classes(self, item: BTItem) -> list[(str, type)]:
        py_name = self.name_to_py(item.item_name)

        #TODO look at Progressive Called Shot/Vigilance cost
        # It goes down but AP can't handle that
        if item.best_allowed_value < item.worst_allowed_value:
            return []
        # TODO ammo bin capacity is dying
        if isinstance(item.best_allowed_value, float):
            return []

        #TODO standardize % as ints, put units in the name (e.g. bulwark damage reduction, ammo bin multiplier)

        min_name = py_name + "_min"
        min_class = type(min_name, (Range, ), {
            "display_name": "Initial " + item.item_name,
            "range_start": item.worst_allowed_value,
            "range_end": item.best_allowed_value,
            "default": item.default_starting_value })
        min_class.__doc__ = item.item_name # TODO new field for this

        max_name = py_name + "_max"
        max_class = type(max_name, (Range, ), {
            "display_name": "Max " + item.item_name,
            "range_start": item.worst_allowed_value,
            "range_end": item.best_allowed_value,
            "default": item.default_best_value })
        max_class.__doc__ = item.item_name # TODO new field for this

        inc_name = py_name + "_inc"
        inc_class = type(inc_name, (Range, ), {
            "display_name": item.item_name + " increment",
            "range_start": 1 if isinstance(item.default_increment, int) else 0.1,
            "range_end": abs(item.best_allowed_value - item.worst_allowed_value),
            "default": item.default_increment })
        max_class.__doc__ = item.item_name # TODO new field for this

        return [(min_name, min_class), (max_name, max_class), (inc_name, inc_class)]

    def make_random_range_classes(self, item: BTItem) -> list[(str, type)]:
        py_name = self.name_to_py(item.item_name)

        min_name = py_name + "_min"
        min_class = type(min_name, (Range, ), {
            "display_name": "Min " + item.item_name,
            "range_start": item.worst_allowed_value,
            "range_end": item.best_allowed_value,
            "default": item.default_starting_value })
        min_class.__doc__ = item.item_name # TODO new field for this

        max_name = py_name + "_max"
        max_class = type(max_name, (Range, ), {
            "display_name": "Max " + item.item_name,
            "range_start": item.worst_allowed_value,
            "range_end": item.best_allowed_value,
            "default": item.default_best_value })
        max_class.__doc__ = item.item_name # TODO new field for this

        return [(min_name, min_class), (max_name, max_class)]

    def make_optional_class(self, item: BTItem) -> list[(str, type)]:
        py_name = self.name_to_py(item.item_name)

        cls = type(py_name, (Choice, ), {
            "display_name": item.item_name,
            "option_starting": BTFindableItemOption.starting.value,
            "option_findable": BTFindableItemOption.findable.value,
            "default": item.default_value.value })
        cls.__doc__ = item.item_name # TODO new field for this

        return [(py_name, cls)]

    def make_range_class(self, item: BTItem) -> list[(str, type)]:
        py_name = self.name_to_py(item.item_name)

        cls = type(py_name, (Range, ), {
            "display_name": item.item_name,
            "range_start": item.worst_allowed_value,
            "range_end": item.best_allowed_value,
            "default": item.default_value })
        cls.__doc__ = item.item_name # TODO new field for this

        return [(py_name, cls)]


# Commented this out until I can look more deeply into how Hollow Knight uses make_dataclass
#options_dataclass = BattleTechOptionsGenerator().options

################################################################################
# Temp options classes

class MinLanceTonnage(Range):
    display_name = "Min Lance Tonnage"
    range_start = 130
    range_end = 400
    default = 200

class MaxLanceTonnage(Range):
    display_name = "Max Lance Tonnage"
    range_start = 130
    range_end = 400
    default = 400

class LanceTonnageIncrement(Range):
    display_name = "Lance Tonnage Increment"
    range_start = 5
    range_end = 100
    default = 10

class MaxMechSlotTonnage(Range):
    range_start = 50
    range_end = 100
    default = 100

class MechSlotTonnageIncrement(Range):
    range_start = 5
    range_end = 100
    default = 10

class MinMechSlot1Tonnage(Range):
    display_name = "Min Mech Slot 1 Tonnage"
    range_start = 45
    range_end = 100
    default = 55

class MaxMechSlot1Tonnage(MaxMechSlotTonnage):
    display_name = "Max Mech Slot 1 Tonnage"

class MechSlot1TonnageIncrement(MechSlotTonnageIncrement):
    display_name = "Mech Slot 1 Tonnage Increment"

class MinMechSlot2Tonnage(Range):
    display_name = "Min Mech Slot 2 Tonnage"
    range_start = 45
    range_end = 100
    default = 45

class MaxMechSlot2Tonnage(MaxMechSlotTonnage):
    display_name = "Max Mech Slot 2 Tonnage"

class MechSlot2TonnageIncrement(MechSlotTonnageIncrement):
    display_name = "Mech Slot 2 Tonnage Increment"

class MinMechSlot3Tonnage(Range):
    display_name = "Min Mech Slot 3 Tonnage"
    range_start = 30
    range_end = 100
    default = 30

class MaxMechSlot3Tonnage(MaxMechSlotTonnage):
    display_name = "Max Mech Slot 3 Tonnage"

class MechSlot3TonnageIncrement(MechSlotTonnageIncrement):
    display_name = "Mech Slot 3 Tonnage Increment"

class MinMechSlot4Tonnage(Range):
    display_name = "Min Mech Slot 4 Tonnage"
    range_start = 20
    range_end = 100
    default = 20

class MaxMechSlot4Tonnage(MaxMechSlotTonnage):
    display_name = "Max Mech Slot 4 Tonnage"

class MechSlot4TonnageIncrement(MechSlotTonnageIncrement):
    display_name = "Mech Slot 4 Tonnage Increment"

@dataclass
class BattleTechHardcodedOptions(PerGameCommonOptions):
    ap_salvage_drop_chance: APSalvageDropChance
    min_lance_tonnage: MinLanceTonnage
    max_lance_tonnage: MaxLanceTonnage
    lance_tonnage_increment: LanceTonnageIncrement
    min_mech_slot_1_tonnage: MinMechSlot1Tonnage
    max_mech_slot_1_tonnage: MaxMechSlot1Tonnage
    mech_slot_1_tonnage_increment: MechSlot1TonnageIncrement
    min_mech_slot_2_tonnage: MinMechSlot2Tonnage
    max_mech_slot_2_tonnage: MaxMechSlot2Tonnage
    mech_slot_2_tonnage_increment: MechSlot2TonnageIncrement
    min_mech_slot_3_tonnage: MinMechSlot3Tonnage
    max_mech_slot_3_tonnage: MaxMechSlot3Tonnage
    mech_slot_3_tonnage_increment: MechSlot3TonnageIncrement
    min_mech_slot_4_tonnage: MinMechSlot4Tonnage
    max_mech_slot_4_tonnage: MaxMechSlot4Tonnage
    mech_slot_4_tonnage_increment: MechSlot4TonnageIncrement

options_dataclass = BattleTechHardcodedOptions
