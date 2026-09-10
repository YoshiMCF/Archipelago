from __future__ import annotations
from typing import TYPE_CHECKING
from .item_data import item_data, BattleTechItemDatum
from .location_data import static_location_data, dynamic_location_data, BattleTechDynamicLocationDatum
from .region_data import region_data, BattleTechRegionDatum
from BaseClasses import ItemClassification as IC


items_to_ids: dict[str, int] = {}
weighted_filler_items: list[BattleTechItemDatum] = []
locations: list[BattleTechStaticLocation | BattleTechDynamicLocation] = []
locations_to_ids: dict[str, int] = {}


for item in item_data:
    items_to_ids[item.item_name] = item.item_id
    if (item.item_classification == IC.filler):
        for i in range(item.filler_weight):
            weighted_filler_items.append(item)

locations = static_location_data.copy()
dynamic_location_count = 100;
for location_index in range(len(dynamic_location_data)):
    location = dynamic_location_data[location_index]
    next_location = dynamic_location_data[location_index+1] \
            if i+1 < len(dynamic_location_data) \
            else None
    if next_location:
        dynamic_location_count = next_location.location_id - location.location_id
    for i in range(dynamic_location_count):
        locations.append(BattleTechDynamicLocationDatum(location.location_id + i, \
                f"{location.location_name} {i}", location.location_type, location.region))

for location in locations:
    locations_to_ids[location.location_name] = location.location_id
