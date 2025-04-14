''' A spaghetti of an abomination to pricess Nissen Data'''
from concurrent.futures import ThreadPoolExecutor
from datetime import date
import pandas as pd
import re
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from utiles.browser import start_headless_chrome_browser
from utiles.lookup import look_for_ref, get_element_text
from utiles.mkdir import mkdir



# Function to scrape product details
def scrape_product(box, driver):

	results = []

	# For every link that is associated to this driver:

	try:

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
		#* Product Info
		########################
		info = look_for_ref(box, '[data-role="offer"]', 0)

		########################
		#* Price Info
		########################
		price = get_element_text(box, 'p"lastoftype', 0)
		print(price)

	except Exception as e:
		print(f"Error processing product, {e}")
		results.append(None)  # Indicate failure

	driver.quit()
	return results


def get_links(pages):

	print("Hello!!")

	# Start the headless Chrome browser (using Selenium)
	driver = start_headless_chrome_browser()

	print("Hello!! After HB")

	results = []

	for key, link in pages.items():

		print(f"Working on {key}...")

		# Opens the link to the site.
		driver.get(link)

		# Close Cookies Thingy...
		try:
			decline_btn = look_for_ref(driver, '#declineButton', 1)
			decline_btn.click()
			print('Closed Cookies!')
		except:
			print("No cookies button found, moving on.")

		sleep(5)

		# Find all classes of links to products
		tiles = driver.find_elements(By.CSS_SELECTOR, '[data-role="offer"]')

		print(len(tiles))

		for tile in tiles:

			########################
			#* Product Info
			########################
			info = look_for_ref(tile, '[data-role="productInformation"]', 0)

			########################
			#* Price Info
			########################
			price = get_element_text(tile, 'p:last-of-type', 0)
			print(price)


		# Append the new links found. This requires figuring out the HTML structure
		# TODO.

	driver.quit()
	return results


def start_coop(n_drivers: int, pages: str) -> pd.DataFrame:

	# Create a pool of drivers
	contents = []

	# One-time pass to map out all links that need to be visited.
	results = get_links(pages)

	# Print the extracted contents
	contents = pd.DataFrame(contents, columns=["Company", "Link", "Product", "Pack Size", "Periodicity", "Type", "OTC", "PAYG", "Subscription", "Date of update"])
	mkdir("./static/scraper/processed")
	contents.to_csv("./static/scraper/processed/Coop.csv")
	print("Coop Done!")
	return contents

# start_coop(5, "https://365discount.coop.dk/365avis/")
