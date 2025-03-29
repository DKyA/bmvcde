''' A spaghetti of an abomination to pricess Nissen Data'''
from concurrent.futures import ThreadPoolExecutor
from datetime import date
import pandas as pd
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from utiles.browser import start_headless_chrome_browser
from utiles.lookup import look_for_ref, get_element_text
from utiles.mkdir import mkdir

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
def scrape_product(indices, hrefs, names):

    results = []

    # Utile predefined Selenium function that sets up the environment.
    driver = start_headless_chrome_browser()

    # For every link that is associated to this driver:
    for index in indices:
        href = hrefs[index]

        try:
            print(f"Working on product no. {index}...")
            driver.get(href)  # Open the link
            # Could be that we will have to implement some counter-detection mechanisms here.

            '''
            The following requires working with the HTML structure of the page. Finding paths to elements
            Where relevant.

            I prepared 2 custom functions, which are safe from Stale references:

            get_element_text(<parent elemenet or driver>, -HTML Identifier-: string, index: int) -> string.
                Useful for finding easily-accessible pieces of text

            look_for_ref(<parent element or driver>, -HTML Identifier-:string, index: int) -> element
                Useful for accessing more difficult information, or finding parents of clusters of information.
                See Period section for example.
            '''


            ########################
            #* Product Name
            ########################
            prod_name = get_element_text(driver, '.product-name1.col', index)

            ########################
            #* Period
            ########################
            t = look_for_ref(driver, '.breadcrumb', index)
            breadcrumb = get_element_text(t, 'li:nth-child(3)', index)
            period = "Monthlies" if "Jatkuvakäyttöiset" in breadcrumb else "Dailies"

            #li:nth-child(3) isn't unique enough. Hence we have to first find the most unique close structure
            #.breadcrumb in this case. And then use that breadcrumb as a base to look for the text

            ########################
            #* Type
            ########################
            focus = "Astigmatism" if "Astigmatism" in prod_name else "Multifocal" if "Multifocal" in prod_name else "Spheric"

            ########################
            #* Packaging support
            ########################
            '''
                This thing requires me to click on a modal to toggle through different packages
                This is done by locating the radio elements (`variation_values`), looping through them,
                and clicking on each button there is (`driver.execute_script("arguments[0].click();", v)`).
                The `v` in the code above being the button of the radio. 
                This then enables me to read off the price.
                Note - Selenium works like human. What is hidden can't be read.
            '''


            control_panel = look_for_ref(driver, '.variation-attribute-text', index)
            variation_values = control_panel.find_elements(By.CLASS_NAME, 'lens-options-select')
            pack_info = control_panel.find_elements(By.CLASS_NAME, 'variation-attribute-select-value')

            payg_price = -10
            for c, v in enumerate(variation_values):
                # Wait for the modal to disappear before clicking each radio button

                n = f"{names[index]}-{c}"
                line = {n: [names[index], href]}

                # Determining the number of lenses in a pack:
                pack_size = pack_info[c].text

                if len(variation_values) > 1:
                    driver.execute_script("arguments[0].click();", v)
                prod_name_adj = prod_name

                pattern = pattern = r'\b\d{1,2}[-]?pack|\b\d{1,2}\s?[a-zA-Z]{1,2}\b|\b\d{1,2}[-]?kpl\b'
                # Yep, this happens... I can recommend regex101, they have a very good sandbox. And Chatgpt is also
                # Quite decent in that, though still not perfect.

                cleaner_name = re.sub(pattern, '', prod_name_adj.lower().replace(' piilolinssit', '').capitalize()).strip()
                line[n].append(ensure_for_astigmatism(cleaner_name)) # Regularizing name to fit standard.

                ##########################
                #* Pack Size
                ##########################
                pack_pattern = r'^\d+'
                line[n].append(re.match(pack_pattern, pack_size).group())

                line[n].append(period)

                line[n].append(focus)

                ########################
                #* OTC Price
                ########################
                line[n].append("") # This is here just for standardization purposes.

                ########################
                #* PAYG Price
                ########################

                # More complex logic to handle discounts.
                # In this application, the request was to keep discounts out, we want them in (simpler usually)

                if len(variation_values) > 1:
                    WebDriverWait(driver, 10).until(lambda driver: get_element_text(driver, '#actual-price', index) != payg_price)
                # Get parent
                parent = look_for_ref(driver, '.prices', index)
                for _ in range(3):      
                    try:
                        prices_avail = get_children(parent, '#actual-price', index)
                        raw_price = prices_avail[-1].text
                        break
                    except StaleElementReferenceException:
                        print(f"Stale found at {prod_name}, id: {index}. Trying again or dying...")
                        continue
                # raw_price = get_element_text(driver, '#actual-price', index)
                price = float(raw_price.replace(" €", "").replace(",", ".").replace('Hinta alennettu\n', '').replace('\nAlennettu hinta', '').strip())
                payg_price = raw_price
                line[n].append(price)


                ########################
                #* Subscription Price
                ########################
                line[n].append(price * 0.8)

                ########################
                #* Time of Update
                ########################
                line[n].append(date.today())

                ########################
                #* Wrap up...
                ########################
                results = results + list(line.values())

                print(f"Product no. {index} done!")

        except Exception as e:
            print(f"Error processing product no. {index}, {prod_name}: {e}")
            results.append(None)  # Indicate failure

    driver.quit()
    return results


def get_links(pages):

    # Start the headless Chrome browser (using Selenium)
    driver = start_headless_chrome_browser()
    hrefs = []
    names = []

    for key, link in pages.items():

        print(f"Working on {key}...")

        # Opens the link to the site.
        driver.get(link)

        # It is important to use these, otherwise you risk stale errors.
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product-grid'))
        )

        # Find all classes of links to products
        tiles = element.find_elements(By.CLASS_NAME, 'product-tile')

        # Append the new links found. This requires figuring out the HTML structure
        hrefs = hrefs + [a.get_attribute('href') for tile in tiles for a in tile.find_elements(By.CSS_SELECTOR, '& > a')]
        names = names + [key for _ in tiles]

    driver.quit()

    print(len(hrefs))
    return [hrefs, names]


def start_silmaasema(n_drivers: int, pages: str) -> pd.DataFrame:

    # Create a pool of drivers
    contents = []

    # Use ThreadPoolExecutor to manage threads
    with ThreadPoolExecutor(max_workers=n_drivers) as executor:

        # One-time pass to map out all links that need to be visited.
        hrefs, names = get_links(pages)

        futures = []
        chunk_size = len(hrefs) // n_drivers  # Determine the chunk size

        # Some optimization for multithreading
        for i in range(n_drivers):
            start_index = i * chunk_size
            end_index = (i + 1) * chunk_size if i < n_drivers - 1 else len(hrefs)
            indices = [j for j in range(start_index, end_index)]

            # This executes the thread loops. scrape_product is the function that does the actual scraping
            futures.append(executor.submit(scrape_product, indices, hrefs, names))

        # Collect results
        for future in futures:
            results = future.result()
            for result in results:
                if result is not None:
                    contents.append(result)

    # Print the extracted contents
    contents = pd.DataFrame(contents, columns=["Company", "Link", "Product", "Pack Size", "Periodicity", "Type", "OTC", "PAYG", "Subscription", "Date of update"])
    mkdir("./static/scraper/processed")
    contents.to_csv("./static/scraper/processed/Silmaasema.csv")
    print("Silmaasema Done!")
    return contents
