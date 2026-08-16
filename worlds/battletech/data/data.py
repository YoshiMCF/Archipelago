from __future__ import annotations
from typing import TYPE_CHECKING
from .item_data import BattleTechItemData, BattleTechItemDatum
from .location_data import BattleTechLocationData, BattleTechDynamicLocationDatum
from BaseClasses import ItemClassification as IC


class BattleTechData:
    # Direct from CSVs
    item_data: BattleTechItemData
    location_data: BattleTechLocationData

    # Derived
    items: list[BattleTechItemDatum]
    items_to_ids: dict[str, int]
    weighted_filler_items: list[BattleTechItemDatum]
    regions: list[str]
    locations: list[BattleTechStaticLocation | BattleTechDynamicLocation]
    locations_to_ids: dict[str, int]

    def __init__(self):
        self.item_data = BattleTechItemData()
        self.location_data = BattleTechLocationData()

        self.items = self.item_data.items
        self.items_to_ids = {}
        for item in self.items:
            self.items_to_ids[item.item_name] = item.item_id
        self.weighted_filler_items = []
        for item in self.items:
            if (item.item_classification == IC.filler):
                for i in range(item.filler_weight):
                    self.weighted_filler_items.append(item)

        self.regions = self.location_data.regions
        self.locations = self.location_data.static_locations.copy()

        dynamic_location_count = 100;
        for location_index in range(len(self.location_data.dynamic_locations)):
            location = self.location_data.dynamic_locations[location_index]
            next_location = self.location_data.dynamic_locations[location_index+1] \
                    if i+1 < len(self.location_data.dynamic_locations) \
                    else None
            if next_location is not None:
                dynamic_location_count = next_location.location_id - location.location_id
            for i in range(dynamic_location_count):
                self.locations.append(BattleTechDynamicLocationDatum(location.location_id + i, \
                        f"{location.location_name} {i}", location.location_type, location.region))

        self.locations_to_ids = {}
        for location in self.locations:
            self.locations_to_ids[location.location_name] = location.location_id

data = BattleTechData()
