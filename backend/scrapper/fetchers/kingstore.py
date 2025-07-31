import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


download_dir = os.path.abspath("downloads")
os.makedirs(download_dir, exist_ok=True)

options = Options()
options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    },
)
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)

driver.get("https://kingstore.binaprojects.com/Main.aspx")

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, "//button[contains(@onclick, 'Download')]")
    )
)

buttons = driver.find_elements(By.XPATH, "//button[contains(@onclick, 'Download')]")

seen = set()
counter = 0
for button in buttons:
    onclick = button.get_attribute("onclick")
    if "Download('" in onclick:
        filename = onclick.split("Download('")[1].split("')")[0]
        if filename in seen:
            continue
        seen.add(filename)
        counter += 1
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        time.sleep(0.5)
        button.click()
        time.sleep(1.5)


driver.quit()

print(f"Done")
