from __future__ import annotations
import csv
from pathlib import Path
from .utils import empty_str_to_none

class BattleTechRegionDatum:
    """
    A row from regions.csv
    """
    region_name: str

    def __init__(self, row: dict[str, str]):
        self.region_name = empty_str_to_none(row["region_name"])

    def validate(self) -> None:
        assert self.region_name

    def __str__(self):
        return str(self.__dict__)


region_data: list[BattleTechRegionDatum] = []

def init_regions():
    region_names = set()

    path = Path(__file__).parent.joinpath("regions.csv")
    with open(path) as regions_file:
        region_reader = csv.DictReader(regions_file)
        for region_row in region_reader:
            if not region_row["region_name"]:
                continue
            region = BattleTechRegionDatum(region_row)

            region.validate()
            assert region.region_name not in region_names
            region_names.add(region.region_name)

            region_data.append(region)

init_regions()
