from __future__ import annotations
from BaseClasses import ItemClassification as IC
from .item_data import item_data, BattleTechItemDatum
from .location_data import static_location_data, dynamic_location_data, BattleTechLocationDatum, \
        BattleTechStaticLocationDatum, BattleTechDynamicLocationDatum

item_names_to_ids: dict[str, int] = {}
weighted_filler_items: list[BattleTechItemDatum] = []
locations: list[BattleTechLocationDatum] = []
location_names_to_ids: dict[str, int] = {}

for item in item_data:
    item_names_to_ids[item.item_name] = item.item_id
    if item.item_classification == IC.filler:
        assert item.filler_weight, f"Item {item} is filler but has no weight defined"
        for _ in range(item.filler_weight):
            weighted_filler_items.append(item)

locations.extend(static_location_data)
dynamic_location_count = 100
for dyn_location_index, dyn_location in enumerate(dynamic_location_data):
    next_dyn_location = dynamic_location_data[dyn_location_index+1] \
            if dyn_location_index+1 < len(dynamic_location_data) \
            else None
    if next_dyn_location:
        dynamic_location_count = next_dyn_location.location_id - dyn_location.location_id
    for i in range(dynamic_location_count):
        locations.append(BattleTechDynamicLocationDatum(dyn_location.location_id + i, \
                f"{dyn_location.location_name} {i}", dyn_location.location_type, dyn_location.region))

for location in locations:
    location_names_to_ids[location.location_name] = location.location_id
