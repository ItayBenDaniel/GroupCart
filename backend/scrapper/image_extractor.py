import requests
import re
import base64
import os
from bs4 import BeautifulSoup


def download_barcode_image(barcode, output_folder=None):

    if output_folder is None:
        script_dir = os.path.dirname(__file__)
        output_folder = os.path.abspath(
            os.path.join(script_dir, "..", "..", "frontend", "assets", "icons")
        )
    os.makedirs(output_folder, exist_ok=True)

    base_url = "https://chp.co.il/%D7%9E%D7%95%D7%93%D7%99%D7%A2%D7%99%D7%9F-%D7%9E%D7%9B%D7%91%D7%99%D7%9D-%D7%A8%D7%A2%D7%95%D7%AA/0/0/"
    url = f"{base_url}{barcode}/0"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        base64_img_data = None
        img_format = None

        for elem in soup.select("[data-uri]"):
            data_uri = elem.get("data-uri")
            if data_uri and data_uri.startswith("data:image"):
                match = re.match(r"data:image/([a-zA-Z]+);base64,(.+)", data_uri)
                if match:
                    img_format, base64_img_data = match.groups()
                    break

        if not base64_img_data:
            for img in soup.find_all("img"):
                src = img.get("src", "")
                if src.startswith("data:image"):
                    match = re.match(r"data:image/([a-zA-Z]+);base64,(.+)", src)
                    if match:
                        img_format, base64_img_data = match.groups()
                        break

        if not base64_img_data:
            matches = re.findall(
                r"data:image/([a-zA-Z]+);base64,([a-zA-Z0-9+/=]+)", response.text
            )
            if matches:
                img_format, base64_img_data = matches[0]

        if not base64_img_data:
            for td in soup.find_all("td"):
                td_str = str(td)
                if "base64" in td_str:
                    match = re.search(
                        r"data:image/([a-zA-Z]+);base64,([a-zA-Z0-9+/=]+)", td_str
                    )
                    if match:
                        img_format, base64_img_data = match.groups()
                        break

        if base64_img_data:
            if img_format.lower() == "gif":
                return "GIF format ignored."
            binary_data = base64.b64decode(base64_img_data)
            output_path = os.path.join(output_folder, f"{barcode}.{img_format}")
            with open(output_path, "wb") as f:
                f.write(binary_data)
            return f"Image saved to {output_path}"
        else:
            return "No image data found."

    except requests.exceptions.RequestException as e:
        return f"Error requesting the page: {e}"
    except Exception as e:
        return f"Error processing the image: {e}"


if __name__ == "__main__":
    import sys

    barcode = sys.argv[1] if len(sys.argv) > 1 else input("Enter the barcode number: ")
    print(download_barcode_image(barcode))
