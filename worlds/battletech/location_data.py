from __future__ import annotations
from typing import TYPE_CHECKING
import csv
import enum

from . import data

class BattleTechStaticLocationType(enum.Enum):
    """
    Defines a group of Locations in BattleTech
    story: winning a campaign mission
    argo: completing an Argo upgrade
    pilot: getting a pilot to a certain skill threshold
    """
    story = enum.auto()
    argo = enum.auto()
    pilot = enum.auto()

    def from_string(string: str) -> BattleTechStaticLocationType:
        match string.lower():
            case "story":
                return BattleTechStaticLocationType.story
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


def empty_str_to_none(s: str):
    return s if s else None


class BattleTechStaticLocationDatum:
    """
    A row from static_locations.csv
    """
    location_id: int
    location_name: str
    location_type: BattleTechStaticLocationType
    unlocked_region: str | None

    def __init__(self, row: csv.DictReader):
        self.location_id = row["location_id"]
        self.location_name = row["location_name"]
        self.location_type = BattleTechStaticLocationType.from_string(row["location_type"])
        self.unlocked_region = empty_str_to_none(row["unlocked_region"])

    def validate(self) -> None:
        assert self.location_id
        assert self.location_name, f"Location with id {self.location_id} has no name"
        assert self.location_type is not None, f"Location with id {self.location_id} has no type"

    def __str__(self):
        return str(self.__dict__)


class BattleTechDynamicLocationDatum:
    """
    A row from dynamic_locations.csv
    """
    location_id: int
    location_name: str
    location_type: BattleTechDynamicLocationType

    def __init__(self, row: csv.DictReader):
        self.location_id = row["location_id"]
        self.location_name = row["location_name"]
        self.location_type = BattleTechDynamicLocationType.from_string(row["location_type"])

    def validate(self) -> None:
        assert self.location_id
        assert self.location_name, f"Location with id {self.location_id} has no name"
        assert self.location_type is not None, f"Location with id {self.location_id} has no type"

    def __str__(self):
        return str(self.__dict__)


class BattleTechLocationData:
    static_locations: list[BattleTechStaticLocationDatum]
    dynamic_locations: list[BattleTechDynamicLocationDatum]

    def __init__(self):
        from importlib.resources import files

        self.static_locations = []
        self.dynamic_locations = []

        location_ids = set()
        location_names = set()

        with files(data).joinpath("static_locations.csv").open() as static_locations_file:
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

                self.static_locations.append(location)

        with files(data).joinpath("dynamic_locations.csv").open() as dynamic_locations_file:
            location_reader = csv.DictReader(dynamic_locations_file)
            for location_row in location_reader:
                if (not location_row["location_id"]):
                    continue
                location = BattleTechDynamicLocationDatum(location_row)

                location.validate()
                assert location.location_id not in location_ids
                location_ids.add(location.location_id)
                assert location.location_name not in location_names
                location_names.add(location.location_name)

                self.dynamic_locations.append(location)

