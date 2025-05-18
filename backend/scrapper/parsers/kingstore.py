import xml.etree.ElementTree as ET
from typing import List
from backend.schemas.store import StoreCreate
from backend.schemas.store_product import StoreProductCreate
from backend.crud.store import create_store
from backend.crud.store_product import create_store_product
from backend.database import SessionLocal
from backend.models.store import Store
from sqlalchemy.orm import Session


def parse_stores_xml(file_path: str) -> List[StoreCreate]:
    tree = ET.parse(file_path)
    root = tree.getroot()

    chain_id = root.findtext("ChainId", default="0")
    chain_name = str(root.findtext("ChainName", default=""))
    stores = []

    for subchain in root.findall(".//SubChain"):
        subchain_id = str(subchain.findtext("SubChainId", default=""))
        print(f"📦 SubChain ID: {subchain_id}")

        for store in subchain.findall(".//Store"):

            stores.append(
                StoreCreate(
                    store_id=int(store.findtext("StoreId", default="0")),
                    chain_id=chain_id,
                    chain_name=chain_name,
                    subchain_id=subchain_id,
                    name=store.findtext("StoreName", default=""),
                    address=store.findtext("Address", default=""),
                    city=store.findtext("City", default=""),
                    latitude="",
                    longitude="",
                )
            )
    for store in stores:
        print(f"{store.chain_id}-{store.subchain_id}-{store.store_id}: {store.name}")
    return stores


def parse_pricefull_xml(file_path: str, db: Session) -> List[StoreProductCreate]:
    tree = ET.parse(file_path)
    root = tree.getroot()

    chain_id = root.findtext("ChainId", default="")
    subchain_id = root.findtext("SubChainId", default="")
    store_id_raw = root.findtext("StoreId", default="0")

    store = (
        db.query(Store)
        .filter_by(
            chain_id=str(chain_id),
            subchain_id=str(subchain_id),
            store_id=int(store_id_raw),
        )
        .first()
    )

    if not store:
        print(f"Store not found: {chain_id}-{subchain_id}-{store_id_raw}")
        return []
    items = []
    for item in root.findall(".//Item"):
        items.append(
            StoreProductCreate(
                store_id=store.id,
                item_code=item.findtext("ItemCode", default=""),
                name=item.findtext("ItemNm", default="Unnamed"),
                manufacturer_name=item.findtext("ManufactureName", default=""),
                manufacturer_country=item.findtext("ManufactureCountry", default=""),
                item_description=item.findtext(
                    "ManufactureItemDescription", default=""
                ),
                unit_quantity=item.findtext("UnitQty", default=""),
                unit_of_measure=item.findtext("UnitOfMeasure", default=""),
                quantity_in_package=item.findtext("QtyInPackage"),
                price=_parse_optional_float(item.findtext("ItemPrice")),
                discounted=item.findtext("AllowDiscount") == "1",
                has_image=False,
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
# print(stores)
# for store in stores:
# create_store(db, store)
db.close()
