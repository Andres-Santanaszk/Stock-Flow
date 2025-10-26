from enum import Enum

class MovType(str, Enum):
    IN = "IN"
    OUT = "OUT"
    ADJUST = "ADJUST"

class ContainerType(str, Enum):
    Rack = "Rack"
    Shelf = "Shelf"
    Bin = "Bin"
    Pallet = "Pallet"
    ScrapArea = "ScrapArea"
    Cart = "Cart"

class ItemType(str, Enum):
    finished_product = "finished_product"
    raw_material = "raw_material"
    component = "component"
    consumable = "consumable"

class UomType(str, Enum):
    Quantity = "Quantity"
    Weight = "Weight"
    Volume = "Volume"
    Length = "Length"
    Area = "Area"
    Time = "Time"

class MovReason(str, Enum):
    purchase = "purchase"
    sale = "sale"
    return_in = "return_in"
    return_out = "return_out"
    scrap = "scrap"
    damage = "damage"
    transfer_in = "transfer_in"
    transfer_out = "transfer_out"
    manufacture_consume = "manufacture_consume"
    manufacture_produce = "manufacture_produce"
