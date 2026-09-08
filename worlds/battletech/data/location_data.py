from __future__ import annotations
from typing import TYPE_CHECKING
import csv
import enum
from pathlib import Path
from .data_utils import parse_int, parse_float, empty_str_to_none
from .region_data import region_data, BattleTechRegionDatum

class BattleTechStaticLocationType(enum.Enum):
    """
    Defines a group of Locations in BattleTech
    story: winning a campaign mission
    event: copy of story, but used by Archipelago to gate regions rather than give rewards
    argo: completing an Argo upgrade
    pilot: getting a pilot to a certain skill threshold
    """
    story = enum.auto()
    event = enum.auto()
    argo = enum.auto()
    pilot = enum.auto()

    def from_string(string: str) -> BattleTechStaticLocationType:
        match string.lower():
            case "story":
                return BattleTechStaticLocationType.story
            case "event":
                return BattleTechStaticLocationType.event
            case "argo":
                return BattleTechStaticLocationType.argo
            case "pilot":
                return BattleTechStaticLocationType.pilot
            case "":
                return None
        assert False, f"Invalid BattleTechStaticLocationType {string}"

class BattleTechDynamicLocationType(enum.Enum):
    """
    Defines a class of repeatable Locations in BattleTech
    salvage: picked from salvage after a mission
    shop: purchased from a shop
    objectives: completed some number of secondary objectives
    contract: completed some number of the given type of contract at certain difficulty levels
    """
    salvage = enum.auto()
    shop = enum.auto()
    objectives = enum.auto()
    contract = enum.auto()

    def from_string(string: str) -> BattleTechDynamicLocationType:
        match string.lower():
            case "salvage":
                return BattleTechDynamicLocationType.salvage
            case "shop":
                return BattleTechDynamicLocationType.shop
            case "objectives":
                return BattleTechDynamicLocationType.objectives
            case "contract":
                return BattleTechDynamicLocationType.contract
            case "":
                return None
        assert False, f"Invalid BattleTechDynamicLocationType {string}"


class BattleTechStaticLocationDatum:
    """
    A row from static_location_data.csv
    """
    location_id: int
    location_name: str
    location_type: BattleTechStaticLocationType
    region: str
    unlocks_region: str | None
    difficulty: int | None

    def __init__(self, row: csv.DictReader):
        self.location_id = int(row["location_id"])
        self.location_name = row["location_name"]
        self.location_type = BattleTechStaticLocationType.from_string(row["location_type"])
        self.region = row["region"] if row["region"] else "Start"
        self.unlocks_region = empty_str_to_none(row["unlocks_region"])
        self.difficulty = parse_int(row["difficulty"])

    def validate(self) -> None:
        assert self.location_id
        assert self.location_name, f"Location with id {self.location_id} has no name"
        assert self.location_type, f"Location with id {self.location_id} has no type"
        assert self.region
        if self.location_type == BattleTechStaticLocationType.event:
            assert isinstance(difficulty, int)
        else:
            assert difficulty == None

    def __str__(self):
        return str(self.__dict__)


class BattleTechDynamicLocationDatum:
    """
    A row from dynamic_location_data.csv
    """
    location_id: int
    location_name: str
    location_type: BattleTechDynamicLocationType
    region: str

    def __init__(self, id: int, name: str, type: BattleTechDynamicLocationType, region: str | None):
        self.location_id = id
        self.location_name = name
        self.location_type = type
        self.region = region

    @classmethod
    def from_csv(cls, row: csv.DictReader):
        location_id = int(row["location_id"])
        location_name = row["location_name"]
        location_type = BattleTechDynamicLocationType.from_string(row["location_type"])
        region = row["region"] if row["region"] else "Start"
        return cls(location_id, location_name, location_type, region)

    def validate(self) -> None:
        assert self.location_id
        assert self.location_name, f"Location with id {self.location_id} has no name"
        assert self.location_type, f"Location with id {self.location_id} has no type"
        assert self.region

    def __str__(self):
        return str(self.__dict__)


static_location_data: list[BattleTechStaticLocationDatum] = []
dynamic_location_data: list[BattleTechDynamicLocationDatum] = []

def init_locations():
    location_ids: set[int] = set()
    location_names: set[str] = set()
    region_names: set[str] = set(map(lambda r: r.region_name, region_data))

    static_path = Path(__file__).parent.joinpath("static_locations.csv")
    with open(static_path) as static_locations_file:
        location_reader = csv.DictReader(static_locations_file)
        for location_row in location_reader:
            if (not location_row["location_id"]):
                continue
            location = BattleTechStaticLocationDatum(location_row)

            location.validate()
            assert location.location_id not in location_ids
            location_ids.add(location.location_id)
            assert location.location_name not in location_names
            location_names.add(location.location_name)

            assert location.region in region_names, \
                    f"Static location {location.location_id}: " + \
                    f"Region {location.unlocks_region} is not in {region_names}"
            if (location.unlocks_region):
                assert location.unlocks_region in region_names, \
                        f"Static location {location.location_id}: " + \
                        f"Region unlock {location.unlocks_region} is not in {region_names}"

            static_location_data.append(location)
    static_location_data.sort(key=lambda loc: loc.location_id)

    dynamic_path = Path(__file__).parent.joinpath("dynamic_locations.csv")
    with open(dynamic_path) as dynamic_locations_file:
        location_reader = csv.DictReader(dynamic_locations_file)
        for location_row in location_reader:
            if (not location_row["location_id"]):
                continue
            location = BattleTechDynamicLocationDatum.from_csv(location_row)

            location.validate()
            assert location.location_id not in location_ids
            location_ids.add(location.location_id)
            assert location.location_name not in location_names
            location_names.add(location.location_name)

            if (location.region):
                assert location.region in region_names, \
                        f"Dynamic location {location.location_id}: " + \
                        f"Region {location.region} is not in {region_names}"

            dynamic_location_data.append(location)
    dynamic_location_data.sort(key=lambda loc: loc.location_id)

    assert static_location_data[-1].location_id < dynamic_location_data[0].location_id

init_locations()
