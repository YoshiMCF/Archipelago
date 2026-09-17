from dataclasses import dataclass
from typing import Any
from Options import OptionGroup, PerGameCommonOptions, Range, Toggle
from .data.item_data import item_data
from .data import constants


class ItemDrivenRange(Range):
    """Range option driven by an item in data/items.csv"""
    display_name = ""
    range_start = 0
    range_end = 0
    default = 0
    def __init__(self, item_id: int):
        item = next(x for x in item_data if x.item_id == item_id)
        assert item.min_option_value is not None, f"No min option value for {item}"
        self.range_start = item.min_option_value
        assert item.max_option_value is not None, f"No max option value for {item}"
        self.range_end = item.max_option_value
        assert item.default_option_value is not None, f"No default option value for {item}"
        self.__class__.default = item.default_option_value
        super().__init__(item.default_option_value)


class ItemDrivenToggle(Toggle):
    """Toggle option driven by an item in data/items.csv"""
    display_name = ""
    default = 0
    def __init__(self, item_id: int):
        item = next(x for x in item_data if x.item_id == item_id)
        assert item.default_option_value in [0, 1]
        self.__class__.default = item.default_option_value
        super().__init__(item.default_option_value)

class MechSlot1StartingTonnage(ItemDrivenRange):
    """Starting max tonnage for mech slot 1"""
    display_name = "Mech Slot 1 Starting Tonnage"
    def __init__(self) -> None:
        super().__init__(constants.MECH_SLOT_TONNAGE_ITEM_IDS[0])


class MechSlot2StartingTonnage(ItemDrivenRange):
    """Starting max tonnage for mech slot 2"""
    display_name = "Mech Slot 2 Starting Tonnage"
    def __init__(self) -> None:
        super().__init__(constants.MECH_SLOT_TONNAGE_ITEM_IDS[1])


class MechSlot3StartingTonnage(ItemDrivenRange):
    """Starting max tonnage for mech slot 3"""
    display_name = "Mech Slot 3 Starting Tonnage"
    def __init__(self) -> None:
        super().__init__(constants.MECH_SLOT_TONNAGE_ITEM_IDS[2])


class MechSlot4StartingTonnage(ItemDrivenRange):
    """Starting max tonnage for mech slot 4"""
    display_name = "Mech Slot 4 Starting Tonnage"
    def __init__(self) -> None:
        super().__init__(constants.MECH_SLOT_TONNAGE_ITEM_IDS[3])


class LanceStartingTonnage(ItemDrivenRange):
    """Starting max tonnage for the entire lance"""
    display_name = "Lance Starting Tonnage"
    def __init__(self) -> None:
        super().__init__(constants.LANCE_TONNAGE_ITEM_ID)


class AutoScoutArgoLocations(Toggle):
    """Automatically scout Argo upgrade locations"""
    display_name = "Auto Scout Argo Upgrades"
    default = 1


class AutoScoutSalvageLocations(Toggle):
    """Show item names when choosing Archipelago item salvage"""
    display_name = "Auto Scout Salvage"
    default = 1


class APSalvageDropChance(Range):
    """
    Percentage chance of finding an Archipelago item in post-mission salvage.
    Not yet implemented.
    """
    display_name = "Archipelago Salvage Drop Chance"
    range_start = 5
    range_end = 100
    default = 25


class CashRewardAmount(ItemDrivenRange):
    """How much cash to award from a Cash item"""
    display_name = "Cash Reward Amount"
    def __init__(self) -> None:
        super().__init__(constants.CASH_ITEM_ID)


class PilotXPRewardAmount(ItemDrivenRange):
    """How much cash to award from a Cash item"""
    display_name = "Cash Reward Amount"
    def __init__(self) -> None:
        super().__init__(constants.PILOT_XP_ITEM_ID)


class MoraleRewardAmount(ItemDrivenRange):
    """How much morale to award from a Morale item"""
    display_name = "Morale Reward Amount"
    def __init__(self) -> None:
        super().__init__(constants.MORALE_ITEM_ID)


class HighSpiritsRewardDuration(ItemDrivenRange):
    """How long to award High Spirits to a pilot when that item is awarded"""
    display_name = "High Spirits Reward Duration"
    def __init__(self) -> None:
        super().__init__(constants.HIGH_SPIRITS_ITEM_ID)


class TechPointsRewardAmount(ItemDrivenRange):
    """How many tech points to award from a Tech Points item"""
    display_name = "Tech Points Reward Amount"
    def __init__(self) -> None:
        super().__init__(constants.TECH_POINTS_ITEM_ID)


class MedPointsRewardAmount(ItemDrivenRange):
    """How many med points to award from a Med Points item"""
    display_name = "Med Points Reward Amount"
    def __init__(self) -> None:
        super().__init__(constants.MED_POINTS_ITEM_ID)


class XPPerDayRewardAmount(ItemDrivenRange):
    """How much passive XP per day, per item"""
    display_name = "XP Per Day Reward Amount"
    def __init__(self) -> None:
        super().__init__(constants.XP_PER_DAY_ITEM_ID)


class XPCapRewardAmount(ItemDrivenRange):
    """How high is the passive XP cap, per item"""
    display_name = "XP Cap Reward Amount"
    def __init__(self) -> None:
        super().__init__(constants.XP_CAP_ITEM_ID)


class ArgoDriveSpeedMultiplier(ItemDrivenRange):
    """How much faster does the Argo fly per item, in %"""
    display_name = "Argo Drive Speed % Reward Amount"
    def __init__(self) -> None:
        super().__init__(constants.ARGO_DRIVE_SPEED_ITEM_ID)


class JumpJets(ItemDrivenToggle):
    """Does the player start with the ability to use jump jets?"""
    display_name = "Start With Jump Jets"
    def __init__(self) -> None:
        super().__init__(constants.JUMP_JETS_ITEM_ID)


class PrecisionShot(ItemDrivenToggle):
    """Does the player start with the ability to use Precision Shot??"""
    display_name = "Start With Precision Shot"
    def __init__(self) -> None:
        super().__init__(constants.PRECISION_SHOT_ITEM_ID)

class Vigilance(ItemDrivenToggle):
    """Does the player start with the ability to use Vigilance??"""
    display_name = "Start With Vigilance"
    def __init__(self) -> None:
        super().__init__(constants.VIGILANCE_ITEM_ID)

# TODO other abilities

@dataclass
class BattleTechOptions(PerGameCommonOptions):
    """All options for generating a BattleTech AP world"""
    mech_slot_1_starting_tonnage: MechSlot1StartingTonnage
    mech_slot_2_starting_tonnage: MechSlot2StartingTonnage
    mech_slot_3_starting_tonnage: MechSlot3StartingTonnage
    mech_slot_4_starting_tonnage: MechSlot4StartingTonnage
    lance_starting_tonnage: LanceStartingTonnage
    auto_scout_argo_locations: AutoScoutArgoLocations
    auto_scout_salvage_locations: AutoScoutSalvageLocations
    ap_salvage_drop_chance: APSalvageDropChance
    cash_reward_amount: CashRewardAmount
    pilot_xp_reward_amount: PilotXPRewardAmount
    morale_reward_amount: MoraleRewardAmount
    high_spirits_reward_duration: HighSpiritsRewardDuration
    tech_points_reward_amount: TechPointsRewardAmount
    med_points_reward_amount: MedPointsRewardAmount
    xp_per_day_reward_amount: XPPerDayRewardAmount
    xp_cap_reward_amount: XPCapRewardAmount
    argo_drive_speed_multiplier: ArgoDriveSpeedMultiplier
    jump_jets: JumpJets
    precision_shot: PrecisionShot
    vigilance: Vigilance
    #TODO other abilities

option_groups = [
    OptionGroup(
        "Starting Tonnage",
        [MechSlot1StartingTonnage, MechSlot2StartingTonnage, MechSlot3StartingTonnage, MechSlot4StartingTonnage, \
                LanceStartingTonnage]
    ),
    OptionGroup(
        "Scouting",
        [AutoScoutArgoLocations, AutoScoutSalvageLocations]
    ),
    OptionGroup(
        "Rewards",
        [CashRewardAmount, PilotXPRewardAmount, MoraleRewardAmount, HighSpiritsRewardDuration, \
                TechPointsRewardAmount, MedPointsRewardAmount, XPPerDayRewardAmount, XPCapRewardAmount, \
                ArgoDriveSpeedMultiplier]
    ),
    OptionGroup(
        "Starting Abilities",
        [JumpJets, PrecisionShot, Vigilance] #TODO
    )
]


# Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
option_presets: dict[str, dict[str, Any]] = {
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
