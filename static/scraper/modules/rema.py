''' A spaghetti of an abomination to pricess Nissen Data'''
from concurrent.futures import ThreadPoolExecutor
from datetime import date
import pandas as pd
import os
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from utiles.browser import start_headless_chrome_browser
from utiles.lookup import look_for_ref, get_element_text #get_element_text_local, look_for_ref_local
from utiles.mkdir import mkdir

       
def look_for_ref_local(parent, selector: str, index: int):
    for _ in range(3):  # Retry up to 3 times
        try:
            res = WebDriverWait(parent, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return res
        except (StaleElementReferenceException, TimeoutException) as e:
            print(f"[WARN] Could not find '{selector}' at index {index}: {e}")
            continue
    return None

def get_element_text_local(parent, selector: str, index: int):
    for _ in range(3):  # Retry up to 3 times
        try:
            element = look_for_ref(parent, selector, index)
            if element:
                return element.text.strip()
        except (StaleElementReferenceException, TimeoutException) as e:
            print(f"[WARN] Could not get text for '{selector}' at index {index}: {e}")
            continue
    return None


def ensure_for_astigmatism(name):
    # Split the name into words
    words = name.split()

    # Check if the last word is "astigmatism"
    if words and words[-1].lower() == "astigmatism":
        # Check if the word before "astigmatism" is "for"
        if len(words) > 1 and words[-2].lower() != "for":
            # Add "for" before "astigmatism"
            words.insert(-1, "for")

    # Join the words back into a single string
    return ' '.join(words)


def get_children(d, cl: str, index: int):
    for _ in range(3):  # Retry up to 3 times
        try:
            children = d.find_elements(By.CSS_SELECTOR, cl)  # Get all child elements
            return children  # Return the number of child elements
        except StaleElementReferenceException:
            print(f"Stale Found on {index}. Trying to get number of children again...")
            continue  # Retry if stale
    return None  # Return 0 if unable to find the number of children after retries



# Function to scrape product details
def scrape_product_rema(indices, hrefs, names):

    results = []
    driver = start_headless_chrome_browser()

    if not indices:
        return []
    index = indices[0]  # Use first index for the common category URL.
    href = hrefs[index]
    greater_category = names[index]

    print(f"Working on product no. {index}...")
    driver.get(href)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.wrap'))
    )
    wraps = driver.find_elements(By.CSS_SELECTOR, 'div.wrap')

    for wrap_index, wrap in enumerate(wraps):
        try:
            # --- Extract lesser category names (e.g., Baguette/flutes) ---
            lesser_category = wrap.find_element(By.CSS_SELECTOR, '.header .title').get_attribute("innerText").strip()
        except Exception as e:
            print(f"Could not find lesser category in wrap {wrap_index}: {e}")
            lesser_category = "N/A"

        # Find product tiles inside this wrap (inside the slider now)
        products = wrap.find_elements(By.CSS_SELECTOR, '.slider .product')

        for i, tile in enumerate(products):
            # Skip '-more' tiles
            tile_class = tile.get_attribute("class")
            if "product--more" in tile_class:
                print(f"Skipping tile {i} (more tile).")
                continue
            
            #THE HOLY GRAIL--------------
            #############################################
            # Ensure the tile is 'scrolled into view' before extracting data
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", tile)
            except Exception as e:
                print(f"Scroll error on tile {i}: {e}")
            ##############################################
            #THE HOLY GRAIL-------------
            
            # --- Extract Product Title ---
            try:
                # Directly get the inner text from the title element within .info
                title_el = tile.find_element(By.CSS_SELECTOR, '.info .title')
                prod_name = title_el.get_attribute("innerText").strip()
                print(f"Raw title text for tile {i}: '{prod_name}'")
                if not prod_name:
                    print(f"[WARN] Empty product name for tile {i}. Tile HTML:\n{tile.get_attribute('outerHTML')}")
                    prod_name = "N/A"
            except Exception as e:
                print(f"Could not parse title for tile {i}: {e}")
                print("Tile HTML:", tile.get_attribute("outerHTML"))
                prod_name = "N/A"

            # --- Extract Price ---
            try:
                price_lmnt = tile.find_element(By.CSS_SELECTOR, '.price .price-normal')
                inner = price_lmnt.get_attribute("innerHTML")
                price_text = price_lmnt.get_attribute("innerText").strip().replace("\n", " ")
                m = re.search(r'(\d+).*?<span.*?>(\d+)', inner)
                if m:
                    payg_price = m.group(1) + "." + m.group(2)
                else:
                    parts = price_text.split()
                    if len(parts) >= 2:
                        payg_price = parts[0] + "." + parts[1]
                    elif parts:
                        payg_price = parts[0]
                    else:
                        print(f"[WARN] Empty price text for tile {i}")
                        payg_price = "N/A"
            except Exception as e:
                print(f"Could not parse price for tile {i} ({prod_name}): {e}")
                print("Tile HTML:", tile.get_attribute("outerHTML"))
                payg_price = "N/A"

            # --- Extract Labels ---
            try:
                label_elements = tile.find_elements(By.CSS_SELECTOR, '.labels-bottom .label')
                labels = ', '.join([lbl.get_attribute("innerText").strip() for lbl in label_elements if lbl.get_attribute("innerText").strip()])
                if not labels:
                    labels = "None"
            except Exception as e:
                print(f"Could not parse labels for tile {i} ({prod_name}): {e}")
                labels = "N/A"

            subscription_price = payg_price  # For now, use the same price

            # --- Build Output Row ---            
            line = [
                "Rema1000",         # Company (static)
                greater_category,   # Greater category from rema_pages
                lesser_category,    # Lesser category from the wrap headers
                href,               # Link to the category page (maybe not needed)
                prod_name,          # Product name
                payg_price,         # PAYG price
                subscription_price, # Subscription price (same for now)
                labels,             # Labels (if any)
                date.today()        # Date of update
            ]
            results.append(line)
            print(f"Scraped: '{prod_name}' with price '{payg_price}' and labels '{labels}'")

    driver.quit()
    return results



def get_links_rema(pages):
    driver = start_headless_chrome_browser()
    hrefs = []
    names = []

    for key, link in pages.items():
        print(f"Working on {key}...")
        driver.get(link)

        # Wait for product tiles to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.product'))
        )

        tiles = driver.find_elements(By.CSS_SELECTOR, 'div.product')
        for tile in tiles:
            try:
                # Skip tiles that are "more" links. They have an extra class "product--more".
                tile_class = tile.get_attribute("class")
                if "product--more" in tile_class:
                    continue

                # Normally, a product tile has a .title element (inside the .info container).
                # You could extract a sample title for debugging—but here we want the overall category.
                hrefs.append(link)  # There’s no unique product URL, so use the category URL.
                names.append(key)   # Use the page/category key (e.g., "Brød og bageri")
            except Exception as e:
                print(f"Could not parse a product tile: {e}")
        # End for tiles in one page.
    driver.quit()
    print(f"Total product links collected: {len(hrefs)}")
    return [hrefs, names]
#^^The above function is a one-time pass to map out all links but if we^^ 
# continue with this surface-level category link for rema wares it can be optimized...



def start_rema(n_drivers: int, pages: str) -> pd.DataFrame:

    # Create a pool of drivers
    contents = []

    # Use ThreadPoolExecutor to manage threads
    with ThreadPoolExecutor(max_workers=n_drivers) as executor:

        # One-time pass to map out all links that need to be visited.
        hrefs, names = get_links_rema(pages)

        futures = []
        chunk_size = len(hrefs) // n_drivers  # Determine the chunk size

        # Some optimization for multithreading
        for i in range(n_drivers):
            start_index = i * chunk_size
            end_index = (i + 1) * chunk_size if i < n_drivers - 1 else len(hrefs)
            indices = [j for j in range(start_index, end_index)]

            # This executes the thread loops. scrape_product is the function that does the actual scraping
            futures.append(executor.submit(scrape_product_rema, indices, hrefs, names))

        # Collect results
        for future in futures:
            results = future.result()
            for result in results:
                if result is not None:
                    contents.append(result)

    # Print the extracted contents
    contents = pd.DataFrame(contents, columns=[
    "Company", "Greater Category", "Type", "Link",
    "Product", "PAYG", "Subscription", "Labels", "Date of update"
])
    mkdir("./static/scraper/processed")
    contents.to_csv("./static/scraper/processed/Rema.csv")
    print("Rema Done!")
    return contents