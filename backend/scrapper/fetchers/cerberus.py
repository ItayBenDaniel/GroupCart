import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

chains = [
    # {
    #     "name": "rami_levi",
    #     "username": "RamiLevi",
    #     "login_url": "https://url.publishedprices.co.il/login",
    #     "download_url": "https://url.publishedprices.co.il/file",
    #     "download_dir": "downloads/rami_levi",
    # },
    # {
    #     "name": "dor_alon",
    #     "username": "doralon",
    #     "login_url": "https://url.publishedprices.co.il/login",
    #     "download_url": "https://url.publishedprices.co.il/file",
    #     "download_dir": "downloads/dor_alon",
    # },
    {
        "name": "tiv_taam",
        "username": "TivTaam",
        "login_url": "https://url.publishedprices.co.il/login",
        "download_url": "https://url.publishedprices.co.il/file",
        "download_dir": "downloads/tiv_taam",
    },
    # {
    #     "name": "yohananof",
    #     "username": "yohananof",
    #     "login_url": "https://url.publishedprices.co.il/login",
    #     "download_url": "https://url.publishedprices.co.il/file",
    #     "download_dir": "downloads/yohananof",
    # },
    # {
    #     "name": "Stop_Market",
    #     "username": "Stop_Market",
    #     "login_url": "https://url.publishedprices.co.il/login",
    #     "download_url": "https://url.publishedprices.co.il/file",
    #     "download_dir": "downloads/Stop_Market",
    # },
    # {
    #     "name": "politzer",
    #     "username": "politzer",
    #     "login_url": "https://url.publishedprices.co.il/login",
    #     "download_url": "https://url.publishedprices.co.il/file",
    #     "download_dir": "downloads/politzer",
    # },
    # {
    #     "name": "Keshet",
    #     "username": "Keshet",
    #     "login_url": "https://url.publishedprices.co.il/login",
    #     "download_url": "https://url.publishedprices.co.il/file",
    #     "download_dir": "downloads/Keshet",
    # },
]


def setup_driver():
    options = Options()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--headless=new")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36"
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def scrape_chain(chain):
    print(f"Scraping chain: {chain['name']}")

    driver = setup_driver()
    driver.delete_all_cookies()

    driver.get(chain["login_url"])
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        driver.find_element(By.NAME, "username").send_keys(chain["username"])
        driver.find_element(By.NAME, "password").send_keys("")
        driver.find_element(By.XPATH, "//button[contains(text(),'Sign in')]").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href^='/file/d/']"))
        )
    except Exception as e:
        print(f"Login or redirect failed: {e}")
        driver.quit()
        return

    driver.get(chain["download_url"])
    time.sleep(4)
    elements = driver.find_elements(By.CSS_SELECTOR, "a[href^='/file/d/']")
    file_links = [e.get_attribute("href") for e in elements]
    print(f"Found {len(file_links)} files.")

    cookies = driver.get_cookies()
    session = requests.Session()

    session.verify = False

    for cookie in cookies:
        session.cookies.set(cookie["name"], cookie["value"])

    os.makedirs(chain["download_dir"], exist_ok=True)
    for url in file_links:
        if "Store" in url:
            continue
        if "Promo" not in url and "Price" not in url:
            continue
        filename = url.split("/")[-1]
        print(f"Downloading {filename}")

        try:
            res = session.get(url, verify=False, timeout=30)
            if res.ok:
                with open(os.path.join(chain["download_dir"], filename), "wb") as f:
                    f.write(res.content)
                print(f"Successfully downloaded {filename}")
            else:
                print(f"Failed to download {filename} ({res.status_code})")
        except requests.exceptions.SSLError as e:
            print(f"SSL Error downloading {filename}: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Request Error downloading {filename}: {e}")

    driver.quit()
    print(f"Done with {chain['name']}")


if __name__ == "__main__":
    for chain in chains:
        try:
            scrape_chain(chain)
        except Exception as e:
            print(f"Error scraping {chain['name']}: {e}")
