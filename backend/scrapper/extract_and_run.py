import gzip
import zipfile
import os
from backend.scrapper.parser import parse_stores_xml, parse_pricefull_xml
from backend.crud.store import create_store
from backend.crud.store_product import create_store_product
from backend.database import SessionLocal


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
        print("Inserting stores")
        stores = parse_stores_xml(xml_path)
        print(f"STORES {stores}")
        for store in stores:
            create_store(db, store)

    # elif "PriceFull" in file_path:
    # products = parse_pricefull_xml(xml_path)
    # for product in products:
    # create_store_product(db, product)

    # elif "Price" in file_path:
    # products = parse_pricefull_xml(xml_path)
    # for product in products:
    # Just update price field
    # create_store_product(db, product)

    db.close()


def run_all(folder: str):
    for file in os.listdir(folder):
        if file.endswith(".gz"):
            full_path = os.path.join(folder, file)
            process_file(full_path)


run_all("downloads/")
