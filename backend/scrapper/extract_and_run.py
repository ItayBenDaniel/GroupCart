import gzip
import zipfile
import os

from backend.scrapper.parsers.cerberus import (
    parse_stores_xml,
    parse_pricefull_xml,
    parse_promotions_xml,
)

from backend.crud.store import create_store
from backend.crud.store_product import create_store_product, add_promos
from backend.database import SessionLocal
from sqlalchemy.orm import Session


def extract_file(file_path: str) -> str:
    with open(file_path, "rb") as f:
        magic = f.read(2)

    if magic == b"PK":
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(os.path.dirname(file_path))
            for name in zip_ref.namelist():
                if name.endswith(".xml"):
                    return os.path.join(os.path.dirname(file_path), name)

    elif magic == b"\x1f\x8b":
        xml_path = file_path.replace(".gz", ".xml")
        with gzip.open(file_path, "rb") as f_in:
            with open(xml_path, "wb") as f_out:
                f_out.write(f_in.read())
        return xml_path

    else:
        raise Exception(f"Unknown file format for: {file_path}")


def process_file(file_path: str):
    db = SessionLocal()
    if "StoresFull" not in file_path and "Stores" not in file_path:
        xml_path = extract_file(file_path)

    if "StoresFull" in file_path or "Stores" in file_path:
        stores = parse_stores_xml(file_path)
        for store in stores:
            create_store(db, store)

    elif "PriceFull" in file_path:
        products = parse_pricefull_xml(xml_path, db)
        for product in products:
            create_store_product(db, product)

    elif "Price" in file_path:
        products = parse_pricefull_xml(xml_path, db)
        for product in products:
            create_store_product(db, product)
    if "PromoFull" in file_path:
        store_id, chain_id, promos = parse_promotions_xml(xml_path)
        add_promos(db, store_id, chain_id, promos)
    db.close()


def run_all(folder: str):

    files = sorted(os.listdir(folder))

    for file in files:
        if "StoresFull" in file or "Stores" in file:
            print(f"🧾 Adding store from {file}")
            process_file(os.path.join(folder, file))
    for file in files:
        if file.endswith("gz"):
            if "PriceFull" in file or "Price" in file:
                process_file(os.path.join(folder, file))
        if file.endswith("gz"):
            if "PromoFull" in file:
                process_file(os.path.join(folder, file))


run_all("downloads/tiv_taam/")
