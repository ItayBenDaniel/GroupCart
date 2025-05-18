import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome headless browser
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Start driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Step 1: Go to login page
login_url = "https://url.publishedprices.co.il"
driver.get(login_url)
time.sleep(2)

# Step 2: Fill in login form
driver.find_element(By.NAME, "username").send_keys("RamiLevi")
driver.find_element(By.NAME, "password").send_keys("")  # No password needed
driver.find_element(By.XPATH, "//button[contains(text(),'Sign in')]").click()

# Step 3: Wait for redirect
time.sleep(4)

# Step 4: Navigate to file list page
driver.get("https://url.publishedprices.co.il/file")
time.sleep(4)

# Step 5: Grab file links
elements = driver.find_elements(By.CSS_SELECTOR, "a[href^='/file/d/']")
file_links = [e.get_attribute("href") for e in elements]
print(f"✅ Found {len(file_links)} files.")
# print(f"FILE LINKS ARE : {file_links}")

# Step 6: Pull cookie from Selenium to use in requests
cookies = driver.get_cookies()
session = requests.Session()
for cookie in cookies:
    session.cookies.set(cookie["name"], cookie["value"])

# Step 7: Download each file
os.makedirs("downloads/rami_levi", exist_ok=True)
for url in file_links:
    if "Price" not in url:
        continue
    print(f" URL is {url}")
    filename = url.split("/")[-1]
    print(f" filename is {filename}")

    print(f"⬇️ Downloading {filename}...")
    res = session.get(url)
    if res.ok:
        with open(os.path.join("downloads/rami_levi", filename), "wb") as f:
            f.write(res.content)
    else:
        print(f"❌ Failed to download {filename}, status code: {res.status_code}")

driver.quit()
print("✅ Done downloading all files.")
