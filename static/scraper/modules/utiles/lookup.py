from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException


#* Util function to sanitize and find refernece element
def look_for_ref(d, cl:str, index: int):
    for _ in range(3):  # Retry up to 3 times
        try:
            res = WebDriverWait(d, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, cl))
            )
            return res
        except StaleElementReferenceException:
            print(f"Stale Found on {index}. Trying again or Dying...")
            continue  # Retry if stale


def get_element_text(d, cl: str, index: int):
    for _ in range(3):  # Retry up to 3 times for getting the text
        try:
            element = look_for_ref(d, cl, index)
            if element is not None:
                return element.text  # Return the text if found
        except StaleElementReferenceException:
            print(f"Stale Found on {index}. Trying to get text again...")
            continue  # Retry if stale