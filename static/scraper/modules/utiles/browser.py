from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service  

def start_headless_chrome_browser():

    # Set up the headless Chrome browser
    options = webdriver.ChromeOptions()
    print("Hello AFTER start")
    #options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-features=NetworkService')
    options.add_argument('--remote-debugging-port=0')
    options.add_argument('--window-size=1280,720')

    # Install the ChromeDriver and create the driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    # driver = webdriver.Chrome(options=options)
    return driver
