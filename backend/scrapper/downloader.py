import requests
from bs4 import BeautifulSoup
import os
import gzip
from urllib.parse import urljoin
from datetime import datetime


def crawl_gz_links(base_url: str) -> list[str]:
    """Get all .gz links from the directory page."""
    resp = requests.get(base_url)
    soup = BeautifulSoup(resp.content, "html.parser")

    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.endswith(".gz"):
            full_url = urljoin(base_url, href)
            links.append(full_url)
    return links


def download_and_extract_gz(url: str, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    filename = url.split("/")[-1]
    gz_path = os.path.join(output_dir, filename)
    xml_path = gz_path.replace(".gz", "")

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download {url}")

    with open(gz_path, "wb") as f:
        f.write(response.content)

    with gzip.open(gz_path, "rb") as f_in:
        with open(xml_path, "wb") as f_out:
            f_out.write(f_in.read())

    return xml_path
