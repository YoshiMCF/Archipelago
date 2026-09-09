from __future__ import annotations
from typing import TYPE_CHECKING
from .item_data import BattleTechItemData, BattleTechItemDatum
from .location_data import BattleTechLocationData, BattleTechDynamicLocationDatum
from .region_data import BattleTechRegionData, BattleTechRegionDatum
from BaseClasses import ItemClassification as IC


# Direct from CSVs
item_data: BattleTechItemData = BattleTechItemData()
region_data: BattleTechRegionData = BattleTechRegionData()
location_data: BattleTechLocationData

# Derived
items: list[BattleTechItemDatum] = item_data.items
items_to_ids: dict[str, int] = {}
weighted_filler_items: list[BattleTechItemDatum] = []
regions: list[str] = []
locations: list[BattleTechStaticLocation | BattleTechDynamicLocation]
locations_to_ids: dict[str, int] = {}


for item in items:
    items_to_ids[item.item_name] = item.item_id
    if (item.item_classification == IC.filler):
        for i in range(item.filler_weight):
            weighted_filler_items.append(item)

for region_datum in region_data.regions:
    regions.append(region_datum.region_name)

location_data = BattleTechLocationData(regions)
locations = location_data.static_locations.copy()
dynamic_location_count = 100;
for location_index in range(len(location_data.dynamic_locations)):
    location = location_data.dynamic_locations[location_index]
    next_location = location_data.dynamic_locations[location_index+1] \
            if i+1 < len(location_data.dynamic_locations) \
            else None
    if next_location:
        dynamic_location_count = next_location.location_id - location.location_id
    for i in range(dynamic_location_count):
        locations.append(BattleTechDynamicLocationDatum(location.location_id + i, \
                f"{location.location_name} {i}", location.location_type, location.region))

for location in locations:
    locations_to_ids[location.location_name] = location.location_id
