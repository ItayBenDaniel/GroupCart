import xml.etree.ElementTree as ET
from typing import List
from backend.schemas.store import StoreCreate
from backend.schemas.store_product import StoreProductCreate
from backend.crud.store import create_store
from backend.crud.store_product import create_store_product
from backend.database import SessionLocal


def parse_stores_xml(file_path: str) -> List[StoreCreate]:
    tree = ET.parse(file_path)
    root = tree.getroot()

    chain_id = root.findtext("ChainId", default="0")
    chain_name = root.findtext("ChainName", default="")

    stores = []
    for store in root.findall(".//Store"):
        stores.append(
            StoreCreate(
                store_id=int(store.findtext("StoreId", default="0")),
                chain_id=chain_id,
                chain_name=chain_name,
                name=store.findtext("StoreName", default=""),
                address=store.findtext("Address", default=""),
                city=store.findtext("City", default=""),
                latitude="",  # not present in this file
                longitude="",  # not present in this file
            )
        )
    return stores


def parse_pricefull_xml(file_path: str) -> List[StoreProductCreate]:
    tree = ET.parse(file_path)
    root = tree.getroot()

    store_id = int(root.findtext("StoreId", default="0"))
    chain_id = root.findtext("ChainId", default="")

    items = []
    for item in root.findall(".//Product"):
        items.append(
            StoreProductCreate(
                store_id=store_id,
                item_code=str(item.findtext("ItemCode", default="")),
                name=item.findtext("ItemName", default="Unnamed"),
                manufacturer_name=item.findtext("ManufactureName", default=""),
                manufacturer_country=item.findtext("ManufactureCountry", default=""),
                item_description=item.findtext(
                    "ManufactureItemDescription", default=""
                ),
                unit_quantity=str(item.findtext("UnitQty", default="")),
                quantity_in_package=str(
                    _parse_optional_int(item.findtext("QtyInPackage"))
                ),
                price=_parse_optional_float(item.findtext("ItemPrice")),
                discounted=item.findtext("AllowDiscount") == "1",
            )
        )
    return items


def _parse_optional_float(value: str | None) -> float | None:
    try:
        return float(value) if value else None
    except ValueError:
        return None


def _parse_optional_int(value: str | None) -> int | None:
    try:
        return int(value) if value else None
    except ValueError:
        return None


db = SessionLocal()
# stores = parse_stores_xml("stores1.xml")
products = parse_pricefull_xml("price1.xml")
# print(stores)
# for store in stores:
# create_store(db, store)
for product in products:
    create_store_product(db, product)
db.close()
