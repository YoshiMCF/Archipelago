from __future__ import annotations
from BaseClasses import ItemClassification as IC
from .item_data import item_data, BattleTechItemDatum
from .location_data import static_location_data, dynamic_location_data, BattleTechStaticLocationDatum, \
        BattleTechDynamicLocationDatum

item_names_to_ids: dict[str, int] = {}
weighted_filler_items: list[BattleTechItemDatum] = []
locations: list[BattleTechStaticLocationDatum | BattleTechDynamicLocationDatum] = []
location_names_to_ids: dict[str, int] = {}

for item in item_data:
    item_names_to_ids[item.item_name] = item.item_id
    if item.item_classification == IC.filler:
        for _ in range(item.filler_weight):
            weighted_filler_items.append(item)

locations = static_location_data.copy()
dynamic_location_count = 100
for location_index, location in enumerate(dynamic_location_data):
    next_location = dynamic_location_data[location_index+1] if location_index+1 < len(dynamic_location_data) else None
    if next_location:
        dynamic_location_count = next_location.location_id - location.location_id
    for i in range(dynamic_location_count):
        locations.append(BattleTechDynamicLocationDatum(location.location_id + i, \
                f"{location.location_name} {i}", location.location_type, location.region))

for location in locations:
    location_names_to_ids[location.location_name] = location.location_id
