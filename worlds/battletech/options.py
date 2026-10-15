from dataclasses import dataclass
from typing import Any
from Options import OptionGroup, PerGameCommonOptions, Range, Toggle, Choice
from .data.item_data import item_data, BattleTechItemDatum
from .data import constants


class BattleTechItemRangeInfo:
    """A BattleTechItemDatum, sanitized for use by a Range option"""
    range_start: int
    range_end: int
    default: int
    def __init__(self, item_id: int):
        item: BattleTechItemDatum = next(x for x in item_data if x.item_id == item_id)
        assert item.min_option_value is not None, f"No min option value for {item}"
        self.range_start = item.min_option_value
        assert item.max_option_value is not None, f"No max option value for {item}"
        self.range_end = item.max_option_value
        assert item.default_option_value is not None, f"No default option value for {item}"
        self.default = item.default_option_value


class BattleTechItemToggleInfo:
    """A BattleTechItemDatum, sanitized for use by a Toggle option"""
    default: int
    def __init__(self, item_id: int):
        item: BattleTechItemDatum = next(x for x in item_data if x.item_id == item_id)
        assert item.default_option_value in [0, 1]
        self.default = item.default_option_value


slot1_item = BattleTechItemRangeInfo(constants.MECH_SLOT_TONNAGE_ITEM_IDS[0])
class MechSlot1StartingTonnage(Range):
    """Starting max tonnage for mech slot 1"""
    display_name = "Mech Slot 1 Starting Tonnage"
    range_start = slot1_item.range_start
    range_end = slot1_item.range_end
    default = slot1_item.default


slot2_item = BattleTechItemRangeInfo(constants.MECH_SLOT_TONNAGE_ITEM_IDS[1])
class MechSlot2StartingTonnage(Range):
    """Starting max tonnage for mech slot 2"""
    display_name = "Mech Slot 2 Starting Tonnage"
    range_start = slot2_item.range_start
    range_end = slot2_item.range_end
    default = slot2_item.default


slot3_item = BattleTechItemRangeInfo(constants.MECH_SLOT_TONNAGE_ITEM_IDS[2])
class MechSlot3StartingTonnage(Range):
    """Starting max tonnage for mech slot 3"""
    display_name = "Mech Slot 3 Starting Tonnage"
    range_start = slot3_item.range_start
    range_end = slot3_item.range_end
    default = slot3_item.default


slot4_item = BattleTechItemRangeInfo(constants.MECH_SLOT_TONNAGE_ITEM_IDS[3])
class MechSlot4StartingTonnage(Range):
    """Starting max tonnage for mech slot 4"""
    display_name = "Mech Slot 4 Starting Tonnage"
    range_start = slot4_item.range_start
    range_end = slot4_item.range_end
    default = slot4_item.default

lance_item = BattleTechItemRangeInfo(constants.LANCE_TONNAGE_ITEM_ID)
class LanceStartingTonnage(Range):
    """Starting max tonnage for the entire lance"""
    display_name = "Lance Starting Tonnage"
    range_start = lance_item.range_start
    range_end = lance_item.range_end
    default = lance_item.default


class AutoScoutArgoLocations(Toggle):
    """Show item rewards before starting Argo upgrades"""
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


cash_item = BattleTechItemRangeInfo(constants.CASH_ITEM_ID)
class CashRewardAmount(Choice): # Range options don't do log scales well
    """How much cash to award from a Cash item"""
    display_name = "Cash Reward Amount"
    option_250000   =   250000
    option_500000   =   500000
    option_1000000  =  1000000
    option_2500000  =  2500000
    option_5000000  =  5000000
    option_10000000 = 10000000
    default = cash_item.default
assert cash_item.range_start == CashRewardAmount.option_250000
assert cash_item.range_end == CashRewardAmount.option_10000000
assert cash_item.default in CashRewardAmount.__dict__.values()


pilot_item = BattleTechItemRangeInfo(constants.PILOT_XP_ITEM_ID)
class PilotXPRewardAmount(Choice):
    """How much pilot xp to award from a Pilot XP item"""
    display_name = "Pilot XP Reward Amount"
    option_100   =   100
    option_250   =   250
    option_500   =   500
    option_1000  =  1000
    option_2500  =  2500
    option_5000  =  5000
    option_10000 = 10000
    option_25000 = 25000
    option_50000 = 50000
    default = pilot_item.default
assert pilot_item.range_start == PilotXPRewardAmount.option_100
assert pilot_item.range_end == PilotXPRewardAmount.option_50000
assert pilot_item.default in PilotXPRewardAmount.__dict__.values()


morale_item = BattleTechItemRangeInfo(constants.MORALE_ITEM_ID)
class MoraleRewardAmount(Range):
    """How much morale to award from a Morale item"""
    display_name = "Morale Reward Amount"
    range_start = morale_item.range_start
    range_end = morale_item.range_end
    default = morale_item.default


high_spirits_item = BattleTechItemRangeInfo(constants.HIGH_SPIRITS_ITEM_ID)
class HighSpiritsRewardDuration(Range):
    """How long to award High Spirits to a pilot when that item is awarded"""
    display_name = "High Spirits Reward Duration"
    range_start = high_spirits_item.range_start
    range_end = high_spirits_item.range_end
    default = high_spirits_item.default


tech_points_item = BattleTechItemRangeInfo(constants.TECH_POINTS_ITEM_ID)
class TechPointsRewardAmount(Range):
    """How many tech points to award from a Tech Points item"""
    display_name = "Tech Points Reward Amount"
    range_start = tech_points_item.range_start
    range_end = tech_points_item.range_end
    default = tech_points_item.default


med_points_item = BattleTechItemRangeInfo(constants.MED_POINTS_ITEM_ID)
class MedPointsRewardAmount(Range):
    """How many med points to award from a Med Points item"""
    display_name = "Med Points Reward Amount"
    range_start = med_points_item.range_start
    range_end = med_points_item.range_end
    default = med_points_item.default


xp_per_day_item = BattleTechItemRangeInfo(constants.XP_PER_DAY_ITEM_ID)
class XPPerDayRewardAmount(Choice):
    """How much passive XP per day, per item"""
    display_name = "XP Per Day Reward Amount"
    option_10   =   10
    option_25   =   25
    option_50   =   50
    option_100  =  100
    option_250  =  250
    option_500  =  500
    option_1000 = 1000
    default = xp_per_day_item.default
assert xp_per_day_item.range_start == XPPerDayRewardAmount.option_10
assert xp_per_day_item.range_end == XPPerDayRewardAmount.option_1000
assert xp_per_day_item.default in XPPerDayRewardAmount.__dict__.values()


xp_cap_item = BattleTechItemRangeInfo(constants.XP_CAP_ITEM_ID)
class XPCapRewardAmount(Choice):
    """How high is the passive XP cap, per item"""
    display_name = "XP Cap Reward Amount"
    option_10000  =  10000
    option_25000  =  25000
    option_50000  =  50000
    option_100000 = 100000
    default = xp_cap_item.default
assert xp_cap_item.range_start == XPCapRewardAmount.option_10000
assert xp_cap_item.range_end == XPCapRewardAmount.option_100000
assert xp_cap_item.default in XPCapRewardAmount.__dict__.values()


drive_speed_item = BattleTechItemRangeInfo(constants.ARGO_DRIVE_SPEED_ITEM_ID)
class ArgoDriveSpeedMultiplier(Range):
    """How much faster does the Argo fly per item, in %"""
    display_name = "Argo Drive Speed % Reward Amount"
    range_start = drive_speed_item.range_start
    range_end = drive_speed_item.range_end
    default = drive_speed_item.default


jump_jets_item = BattleTechItemToggleInfo(constants.JUMP_JETS_ITEM_ID)
class JumpJets(Toggle):
    """Does the player start with the ability to use jump jets?"""
    display_name = "Start With Jump Jets"
    default = jump_jets_item.default


precision_shot_item = BattleTechItemToggleInfo(constants.PRECISION_SHOT_ITEM_ID)
class PrecisionShot(Toggle):
    """Does the player start with the ability to use Precision Shot?"""
    display_name = "Start With Precision Shot"
    default = precision_shot_item.default


vigilance_item = BattleTechItemToggleInfo(constants.VIGILANCE_ITEM_ID)
class Vigilance(Toggle):
    """Does the player start with the ability to use Vigilance?"""
    display_name = "Start With Vigilance"
    default = vigilance_item.default


multi_target_item = BattleTechItemToggleInfo(constants.MULTI_TARGET_ITEM_ID)
class MultiTarget(Toggle):
    """Does the player start with the ability for pilots to learn Multi-Target?"""
    display_name = "Start With Multi-Target"
    default = multi_target_item.default


breaching_shot_item = BattleTechItemToggleInfo(constants.BREACHING_SHOT_ITEM_ID)
class BreachingShot(Toggle):
    """Does the player start with the ability for pilots to learn Breaching Shot?"""
    display_name = "Start With Breaching Shot"
    default = breaching_shot_item.default


bulwark_item = BattleTechItemToggleInfo(constants.BULWARK_ITEM_ID)
class Bulwark(Toggle):
    """Does the player start with the ability for pilots to learn Bulwark?"""
    display_name = "Start With Bulwark"
    default = bulwark_item.default


coolant_vent_item = BattleTechItemToggleInfo(constants.COOLANT_VENT_ITEM_ID)
class CoolantVent(Toggle):
    """Does the player start with the ability for pilots to learn Coolant Vent?"""
    display_name = "Start With Coolant Vent"
    default = coolant_vent_item.default


sure_footing_item = BattleTechItemToggleInfo(constants.SURE_FOOTING_ITEM_ID)
class SureFooting(Toggle):
    """Does the player start with the ability for pilots to learn Sure Footing?"""
    display_name = "Start With Sure Footing"
    default = sure_footing_item.default


ace_pilot_item = BattleTechItemToggleInfo(constants.ACE_PILOT_ITEM_ID)
class AcePilot(Toggle):
    """Does the player start with the ability for pilots to learn Ace Pilot?"""
    display_name = "Start With Ace Pilot"
    default = ace_pilot_item.default


sensor_lock_item = BattleTechItemToggleInfo(constants.SENSOR_LOCK_ITEM_ID)
class SensorLock(Toggle):
    """Does the player start with the ability for pilots to learn Sensor Lock?"""
    display_name = "Start With Sensor Lock"
    default = sensor_lock_item.default


master_tactician_item = BattleTechItemToggleInfo(constants.MASTER_TACTICIAN_ITEM_ID)
class MasterTactician(Toggle):
    """Does the player start with the ability for pilots to learn Master Tactician?"""
    display_name = "Start With Master Tactician"
    default = master_tactician_item.default


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
    multi_target: MultiTarget
    breaching_shot: BreachingShot
    bulwark: Bulwark
    coolant_vent: CoolantVent
    sure_footing: SureFooting
    ace_pilot: AcePilot
    sensor_lock: SensorLock
    master_tactician: MasterTactician

option_groups: list[OptionGroup] = [
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
        [JumpJets, PrecisionShot, Vigilance, MultiTarget, BreachingShot, Bulwark, CoolantVent, SureFooting, \
                AcePilot, SensorLock, MasterTactician]
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
