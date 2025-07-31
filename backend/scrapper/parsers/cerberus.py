import xml.etree.ElementTree as ET
from typing import List, Dict
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

    chain_id = root.findtext("ChainID", default="0")
    chain_name = str(root.findtext("ChainName", default=""))
    stores = []

    for subchains in root.findall(".//SubChains"):
        for subchain in subchains.findall(".//SubChain"):
            subchain_id = str(int(subchain.findtext("SubChainID", default="0")))
            print(f"📦 SubChain ID: {subchain_id}")

            for store in subchain.findall(".//Store"):

                stores.append(
                    StoreCreate(
                        store_id=int(store.findtext("StoreID", default="0")),
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
    if chain_id == "":
        chain_id = root.findtext("ChainID", default="")
        if chain_id != "":
            chain_id = str(int(chain_id))
    subchain_id = root.findtext("SubChainId", default="")
    if subchain_id == "":
        subchain_id = root.findtext("SubChainID", default="")
        if subchain_id != "":
            subchain_id = str(int(subchain_id))
    if subchain_id == "0" or subchain_id == "000":
        subchain_id = "1"
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
    for i in root.findall(".//Items"):
        for item in i.findall(".//Item"):
            items.append(
                StoreProductCreate(
                    store_id=store.id,
                    item_code=item.findtext("ItemCode", default=""),
                    name=item.findtext("ItemName", default="Unnamed"),
                    manufacturer_name=item.findtext("ManufacturerName", default=""),
                    manufacturer_country=item.findtext(
                        "ManufactureCountry", default=""
                    ),
                    item_description=item.findtext(
                        "ManufacturerItemDescription", default=""
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


def parse_promotions_xml(file_path: str) -> Dict[str, float]:
    tree = ET.parse(file_path)
    root = tree.getroot()
    chain_id = root.findtext("ChainId")
    store_id = root.findtext("StoreId")
    if not chain_id or not store_id:
        return None
    item_discounts = {}

    for promo in root.findall(".//Promotion"):
        discounted_price = promo.findtext("DiscountedPricePerMida")
        if not discounted_price:
            continue
        try:
            unit_price = float(discounted_price)
        except ValueError:
            continue
        for item in promo.findall(".//PromotionItems/Item"):
            item_code = item.findtext("ItemCode")
            if item_code:
                item_discounts[item_code] = unit_price

    return (store_id, chain_id, item_discounts)


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
