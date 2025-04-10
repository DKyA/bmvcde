from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def start_headless_chrome_browser():
    options = Options()
    options.binary_location = r"C:\Program Files\Chromium\Application\chrome.exe"
    options.add_argument('--headless=new')
    options.add_argument('--window-size=1280,720')

    # Optional, but good practice
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(), options=options)

    return driver
