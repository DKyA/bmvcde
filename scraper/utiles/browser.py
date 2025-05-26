
from selenium import webdriver
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  
import tempfile

# This is here so that the code just runs (hopefully :D)
if os.name == "nt":
    import undetected_chromedriver as uc
else:
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


def start_browser():
    '''
    New function for me to start Coop. I started having some issues with Cloudflare
    Protection, this here is to mitigate it :)
    Second part provided for compatibility with Nicklas.
    '''
    print("Starting browser...")
    if os.name == "nt":
        options = uc.ChromeOptions()
        options.binary_location = r"C:\Program Files\Chromium\Application\chrome.exe"
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1280,720')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
        
        driver = uc.Chrome(options=options, version_main=135)
    
    else:
        options = Options()
        options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        user_data_dir = tempfile.mkdtemp()

        options.add_argument('--headless=new')  # Up to you if you want headless on Mac
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-features=NetworkService')
        options.add_argument('--remote-debugging-port=0')
        options.add_argument('--window-size=1280,720')
        options.add_argument(f'--user-data-dir={user_data_dir}')  # temp user data dir

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    # driver.minimize_window()
    print("Browser started.")
    return driver