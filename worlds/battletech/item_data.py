from __future__ import annotations
from typing import TYPE_CHECKING
import csv
import enum

from BaseClasses import ItemClassification as IC
from . import data

class BattleTechItemOptionType(enum.Enum):
    """
    Defines how an item is implemented
    progressive: an item that can be awarded multiple times
    random_range: an item that gives out a random number of sub-items (e.g. laser weapon cache)
    optional: an item that the player either starts with or can find once
    None (empty string): TODO is this different from progressive?
    """
    progressive = enum.auto()
    random_range = enum.auto()
    optional = enum.auto()

    def from_string(string: str) -> ItemOptionType:
        match string.lower():
            case "progressive":
                return BattleTechItemOptionType.progressive
            case "random_range":
                return BattleTechItemOptionType.random_range
            case "optional":
                return BattleTechItemOptionType.optional
            case "":
                return None
        assert False, f"Invalid BattleTechItemOptionType {string}"


class BattleTechItemFindableOptionType(enum.Enum):
    """
    Defines whether an item with BattleTechItemOptionType=optional is available at the start of the game
    or needs to be found.
    """
    starting = enum.auto()
    findable = enum.auto()

    def from_string(string: str) -> ItemFindableOptionType:
        match string.lower():
            case "starting":
                return BattleTechItemFindableOptionType.starting
            case "findable":
                return BattleTechItemFindableOptionType.findable
        assert False, f"Invalid BattleTechItemFindableOptionType {string}"


def ic_from_string(string: str) -> IC:
    match string.lower():
        case "filler":
            return IC.filler
        case "progression":
            return IC.progression
        case "useful":
            return IC.useful
        case "trap":
            return IC.trap
    assert False, f"Invalid ItemClassification {string}"


def empty_str_to_none(s: str):
    return s if s else None

class BattleTechItemDatum:
    """
    A row from items.csv
    """
    item_id: int
    item_name: str
    item_classification: IC
    filler_weight: int | None
    option_type = BattleTechItemOptionType | None
    worst_allowed_value: float | None
    best_allowed_value: float | None
    default_starting_value: float | None
    default_best_value: float | None
    default_increment: float | None
    default_value: float | str | None

    def __init__(self, row: csv.DictReader):
        self.item_id = row["item_id"]
        self.item_name = row["item_name"]
        self.item_classification = ic_from_string(row["item_classification"])
        self.filler_weight = empty_str_to_none(row["filler_weight"])
        self.option_type = BattleTechItemOptionType.from_string(row["option_type"])
        self.worst_allowed_value = empty_str_to_none(row["worst_allowed_value"])
        self.best_allowed_value = empty_str_to_none(row["best_allowed_value"])
        self.default_starting_value = empty_str_to_none(row["default_starting_value"])
        self.default_best_value = empty_str_to_none(row["default_best_value"])
        self.default_increment = empty_str_to_none(row["default_increment"])
        self.default_value = empty_str_to_none(row["default_value"])

    def validate(self) -> None:
        assert self.item_id
        assert self.item_name, f"Item with id {self.item_id} has no name"
        assert self.item_classification is not None, f"Item with id {self.item_id} has no classification"

        if (self.item_classification == IC.filler):
            assert self.filler_weight is not None, \
                    f"Item with id {self.item_id} is filler but has no weight"
        else:
            assert self.filler_weight is None, \
                    f"Item with id {self.item_id} is {self.item_classification} but has filler_weight defined"

        if (self.worst_allowed_value is None):
            assert self.best_allowed_value is None, \
                    f"Item with id {self.itemk_id} has best_allowed_value but no worst_allowed_value"
        else:
            assert self.best_allowed_value is not None, \
                    f"Item with id {self.itemk_id} has worst_allowed_value but no best_allowed_value"
        #TODO validate default_starting_value, default_best_value, default_increment, and default_value
        # and maybe define them better

    def __str__(self):
        return str(self.__dict__)
        #result = ""
        #for attr in dir(self):
        #    result += f"'{attr}'=>'{getattr(self, attr)}' "
        #return result


class BattleTechItemData:
    items: list[BattleTechItemDatum]

    def __init__(self):
        from importlib.resources import files

        self.items = []

        item_ids = set()
        item_names = set()

        with files(data).joinpath("items.csv").open() as items_file:
            item_reader = csv.DictReader(items_file)
            for item_row in item_reader:
                if (not item_row["item_id"]):
                    continue
                item = BattleTechItemDatum(item_row)

                item.validate()
                assert item.item_id not in item_ids
                item_ids.add(item.item_id)
                assert item.item_name not in item_names
                item_names.add(item.item_name)

                self.items.append(item)
