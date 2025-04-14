from selenium import webdriver
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  
import tempfile

# This checks if this runs on Win / MacOS (nt = windows)
# This is here so that the code just runs (hopefully :D)
if os.name != "nt":
    from webdriver_manager.chrome import ChromeDriverManager

def start_headless_chrome_browser():

    # Set up the headless Chrome browser
    if os.name == "nt":
        options = Options()
        options.binary_location = r"C:\Program Files\Chromium\Application\chrome.exe"
    else:
        options = webdriver.ChromeOptions()
        options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        user_data_dir = tempfile.mkdtemp()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-features=NetworkService')
    options.add_argument('--remote-debugging-port=0')
    options.add_argument('--window-size=1280,720')

    if os.name == "nt":
        driver = webdriver.Chrome(options=options)
    else:
        # Install the ChromeDriver and create the driver
        options.add_argument(f'--user-data-dir={user_data_dir}')#temp user data dir
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    return driver
