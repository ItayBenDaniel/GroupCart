import gzip
import zipfile
import os
from backend.scrapper.parser import parse_stores_xml, parse_pricefull_xml
from backend.crud.store import create_store
from backend.crud.store_product import create_store_product
from backend.database import SessionLocal
from sqlalchemy.orm import Session


def extract_file(file_path: str) -> str:
    with open(file_path, "rb") as f:
        magic = f.read(2)

    # ZIP files start with b'PK'
    if magic == b"PK":
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(os.path.dirname(file_path))
            for name in zip_ref.namelist():
                if name.endswith(".xml"):
                    return os.path.join(os.path.dirname(file_path), name)

    # GZ files start with b'\x1f\x8b'
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
    xml_path = extract_file(file_path)

    if "StoresFull" in file_path:
        stores = parse_stores_xml(xml_path)
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

    db.close()


def run_all(folder: str):

    files = sorted(os.listdir(folder))  # optional

    # Do stores first
    for file in files:
        if file.endswith("gz"):
            if "StoresFull" in file:
                print(f"Adding store {file}")
                process_file(os.path.join(folder, file))

    # Then prices
    for file in files:
        if file.endswith("gz"):
            if "PriceFull" in file or "Price" in file:
                process_file(os.path.join(folder, file))

    # Then promos (if applicable)
    for file in files:
        if file.endswith("gz"):
            if "PromoFull" in file:
                process_file(os.path.join(folder, file))


run_all("downloads/")
