from __future__ import annotations
import csv
import enum
import locale
from pathlib import Path
from .utils import parse_int, empty_str_to_none
from .region_data import region_data
from . import constants

class BattleTechStaticLocationType(enum.Enum):
    """
    Defines a group of Locations in BattleTech
    STORY: winning a campaign mission
    EVENT: copy of story, but used by Archipelago to gate regions rather than give rewards
    ARGO: completing an Argo upgrade
    PILOT: getting a pilot to a certain skill threshold
    """
    STORY = enum.auto()
    EVENT = enum.auto()
    ARGO = enum.auto()
    PILOT = enum.auto()

    @staticmethod
    def from_string(string: str) -> BattleTechStaticLocationType:
        match string.lower():
            case "story":
                return BattleTechStaticLocationType.STORY
            case "event":
                return BattleTechStaticLocationType.EVENT
            case "argo":
                return BattleTechStaticLocationType.ARGO
            case "pilot":
                return BattleTechStaticLocationType.PILOT
        assert False, f"Invalid BattleTechStaticLocationType {string}"

class BattleTechDynamicLocationType(enum.Enum):
    """
    Defines a class of repeatable Locations in BattleTech
    SALVAGE: picked from salvage after a mission
    SHOP: Purchased from a shop
    OBJECTIVES: completed some number of secondary objectives
    CONTRACT: completed some number of the given type of contract at certain difficulty levels
    """
    SALVAGE = enum.auto()
    SHOP = enum.auto()
    OBJECTIVES = enum.auto()
    CONTRACT = enum.auto()

    @staticmethod
    def from_string(string: str) -> BattleTechDynamicLocationType:
        match string.lower():
            case "salvage":
                return BattleTechDynamicLocationType.SALVAGE
            case "shop":
                return BattleTechDynamicLocationType.SHOP
            case "objectives":
                return BattleTechDynamicLocationType.OBJECTIVES
            case "contract":
                return BattleTechDynamicLocationType.CONTRACT
        assert False, f"Invalid BattleTechDynamicLocationType {string}"


class BattleTechLocationDatum:
    """Common data from either static or dynamic locations"""
    location_id: int
    location_name: str
    region: str

    def __init__(self, location_id: int, location_name: str, region: str):
        self.location_id = location_id
        self.location_name = location_name
        self.region = region if region else constants.STARTING_REGION

    def validate(self) -> None:
        assert self.location_id
        assert self.location_name, f"Location with id {self.location_id} has no name"
        assert self.region

    def __str__(self) -> str:
        return str(self.__dict__)

class BattleTechStaticLocationDatum(BattleTechLocationDatum):
    """A row from static_location_data.csv"""
    location_id: int
    location_name: str
    location_type: BattleTechStaticLocationType
    region: str
    unlocks_region: str | None
    difficulty: int | None

    def __init__(self, row: dict[str, str]):
        super().__init__(int(row["location_id"]), row["location_name"], row["region"])
        self.location_type = BattleTechStaticLocationType.from_string(row["location_type"])
        self.unlocks_region = empty_str_to_none(row["unlocks_region"])
        self.difficulty = parse_int(row["difficulty"])

    def validate(self) -> None:
        super().validate()
        assert self.location_type, f"Location with id {self.location_id} has no type"
        if self.location_type != BattleTechStaticLocationType.EVENT:
            assert self.unlocks_region is None
        if self.location_type in {BattleTechStaticLocationType.STORY, BattleTechStaticLocationType.EVENT}:
            assert isinstance(self.difficulty, int)
            assert 0 <= self.difficulty and self.difficulty <= constants.DIFFICULTY_LEVELS
        else:
            assert self.difficulty is None


class BattleTechDynamicLocationDatum(BattleTechLocationDatum):
    """A row from dynamic_location_data.csv"""
    location_type: BattleTechDynamicLocationType

    def __init__(self, location_id: int, location_name: str, location_type: BattleTechDynamicLocationType, region: str):
        super().__init__(location_id, location_name, region)
        self.location_type = location_type

    @classmethod
    def from_csv(cls, row: dict[str, str]) -> BattleTechDynamicLocationDatum:
        location_id = int(row["location_id"])
        location_name = row["location_name"]
        location_type = BattleTechDynamicLocationType.from_string(row["location_type"])
        region = row["region"]
        return cls(location_id, location_name, location_type, region)

    def validate(self) -> None:
        super().validate()
        assert self.location_type, f"Location with id {self.location_id} has no type"


static_location_data: list[BattleTechStaticLocationDatum] = []
dynamic_location_data: list[BattleTechDynamicLocationDatum] = []

def init_locations() -> None:
    location_ids: set[int] = set()
    location_names: set[str] = set()
    region_names: set[str] = set(map(lambda r: r.region_name, region_data))

    static_path = Path(__file__).parent.joinpath("static_locations.csv")
    with open(static_path, encoding=locale.getencoding()) as static_locations_file:
        location_reader = csv.DictReader(static_locations_file)
        for location_row in location_reader:
            if not location_row["location_id"]:
                continue
            static_location = BattleTechStaticLocationDatum(location_row)
            static_location.validate()
            assert static_location.location_id not in location_ids
            location_ids.add(static_location.location_id)
            assert static_location.location_name not in location_names
            location_names.add(static_location.location_name)

            assert static_location.region in region_names, \
                    f"Static location {static_location.location_id}: " + \
                    f"Region {static_location.unlocks_region} is not in {region_names}"
            if static_location.unlocks_region:
                assert static_location.unlocks_region in region_names, \
                        f"Static location {static_location.location_id}: " + \
                        f"Region unlock {static_location.unlocks_region} is not in {region_names}"

            static_location_data.append(static_location)
    static_location_data.sort(key=lambda loc: loc.location_id)

    dynamic_path = Path(__file__).parent.joinpath("dynamic_locations.csv")
    with open(dynamic_path, encoding=locale.getencoding()) as dynamic_locations_file:
        location_reader = csv.DictReader(dynamic_locations_file)
        for location_row in location_reader:
            if not location_row["location_id"]:
                continue
            dyn_location = BattleTechDynamicLocationDatum.from_csv(location_row)

            dyn_location.validate()
            assert dyn_location.location_id not in location_ids
            location_ids.add(dyn_location.location_id)
            assert dyn_location.location_name not in location_names
            location_names.add(dyn_location.location_name)

            if dyn_location.region:
                assert dyn_location.region in region_names, \
                        f"Dynamic location {dyn_location.location_id}: " + \
                        f"Region {dyn_location.region} is not in {region_names}"

            dynamic_location_data.append(dyn_location)
    dynamic_location_data.sort(key=lambda loc: loc.location_id)

    assert static_location_data[-1].location_id < dynamic_location_data[0].location_id

init_locations()
