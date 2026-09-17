from __future__ import annotations
import csv
import enum
from pathlib import Path
from BaseClasses import ItemClassification as IC
from .utils import parse_int, parse_float


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
    assert False, f"Invalid ItemClassification '{string}'"


class BattleTechItemDatum:
    """
    A row from items.csv
    """
    item_id: int
    item_name: str
    item_classification: IC
    filler_weight: int | None
    min_option_value: int | None
    default_option_value: int | None
    max_option_value: int | None
    count: int | None

    def __init__(self, row: dict[str, str]):
        self.item_id = int(row["item_id"])
        self.item_name = row["item_name"]
        self.item_classification = ic_from_string(row["item_classification"])
        self.filler_weight = parse_int(row["filler_weight"])
        self.min_option_value = parse_int(row["min_option_value"])
        self.default_option_value = parse_int(row["default_option_value"])
        self.max_option_value = parse_int(row["max_option_value"])
        self.count = parse_int(row["count"])


    def validate(self) -> None:
        assert self.item_id
        assert self.item_name, f"Item with id {self.item_id} has no name"

        if self.item_classification == IC.filler:
            assert self.filler_weight, f"Item with id {self.item_id} is filler but has no weight"
        else:
            assert self.filler_weight is None, \
                    f"Item with id {self.item_id} is {self.item_classification} but has filler_weight defined"

        if self.min_option_value is None:
            assert self.default_option_value is not None, \
                    f"Item with id {self.item_id} has min_option_value but no default_option_value"
            assert self.max_option_value is not None, \
                    f"Item with id {self.item_id} has min_option_value but no max_option_value"
        else:
            assert self.default_option_value is None, \
                    f"Item with id {self.item_id} has default_option_value but no min_option_value"
            assert self.max_option_value is None, \
                    f"Item with id {self.item_id} has max_option_value but no min_option_value"


    def __str__(self):
        return str(self.__dict__)


item_data: list[BattleTechItemDatum] = []

def init_item_data():
    item_ids = set()
    item_names = set()

    path = Path(__file__).parent.joinpath("items.csv")
    with open(path) as items_file:
        item_reader = csv.DictReader(items_file)
        for item_row in item_reader:
            if not item_row["item_id"]:
                continue
            item = BattleTechItemDatum(item_row)

            item.validate()
            assert item.item_id not in item_ids
            item_ids.add(item.item_id)
            assert item.item_name not in item_names
            item_names.add(item.item_name)

            item_data.append(item)

init_item_data()
