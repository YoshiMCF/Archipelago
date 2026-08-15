from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import ItemClassification as IC
from .item_data import BattleTechItemData
from .location_data import BattleTechLocationData

items = BattleTechItemData()
locations = BattleTechLocationData()

weighted_filler_items = [filler for item in items.items
        if (item.item_classification == IC.filler)
        for filler in range(item.filler_weight)]
items_to_ids = {item.item_name: item.item_id for item in items.items}
#TODO expand out dynamic locations
locations_to_ids = {location.location_name: location.location_id for location in locations.static_locations}
