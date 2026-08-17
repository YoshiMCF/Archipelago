from __future__ import annotations
from typing import TYPE_CHECKING
import csv
import enum
from pathlib import Path

from .data_utils import empty_str_to_none

class BattleTechRegionDatum:
    """
    A row from regions.csv
    """
    region_name: str

    def __init__(self, row: csv.DictReader):
        self.region_name = empty_str_to_none(row["region_name"])


    def validate(self) -> None:
        assert self.region_name

    def __str__(self):
        return str(self.__dict__)


class BattleTechRegionData:
    regions: list[BattleTechRegionDatum]

    def __init__(self):
        self.regions = []

        region_names = set()

        path = Path(__file__).parent.joinpath("regions.csv")
        with open(path) as regions_file:
            region_reader = csv.DictReader(regions_file)
            for region_row in region_reader:
                if (not region_row["region_name"]):
                    continue
                region = BattleTechRegionDatum(region_row)

                region.validate()
                assert region.region_name not in region_names
                region_names.add(region.region_name)

                self.regions.append(region)
