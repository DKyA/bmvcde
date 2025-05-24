''' A spaghetti of an abomination to pricess Nissen Data'''
from datetime import date
import pandas as pd
import re
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from utiles.browser import start_browser
from utiles.lookup import look_for_ref, get_element_text
from utiles.mkdir import mkdir

def get_items(tile, info):

	detail = get_element_text(info, 'p:last-of-type', 0)

	pattern = r"^(?:Min[.]?\s)?(\d+\W?\d*)\s(\w+).|([a-zA-Z-]+)\s(\d+)"

	match = re.search(pattern, detail, flags=re.IGNORECASE)
	if match:
		g_1 = match.group(1)
		g_2 = match.group(2)

		if g_1 == "stk-pris":
			quantity = 1
			unit = "pcs"
		else:
			quantity = g_1
			unit = g_2
	else:
		# print(f"Error! Invaild format of Detail Info for {name}; got value: {detail}")
		# So, the things that will fail right now are non-groceries in nature. I will therefore take the liberty to skip them :)
		return []
		# I will not elaborate.

	########################
	#* Price Info
	########################
	price_el = look_for_ref(tile, 'p[data-single-line="true"]', 0)
	price = price_el.text

	pattern = r"(\d+),-"
	match = re.search(pattern, price, flags=re.IGNORECASE)
	if match:
		price = match.group(1)
	# Else = the price for some reason doesn't have `,-`, no action needed.

	# This peiece checks if there is the decimal part of the number as to properly format it.
	try:
		price_el.find_element(By.TAG_NAME, 'span')
		price = int(price) / 100
		print(f"Decimal detected! I adjusted the price to {price}.")
	except NoSuchElementException:
		pass
		# Nothing needs to be done - this is already correct
		# (I hate try/except, if is so much better. Fuck halting problem)

	########################
	#* Img Info
	########################
	img = look_for_ref(tile, 'img', 0).get_attribute('src')

	return [price, "", img, "", quantity, unit]


def scrape(pages):

	# Start the headless Chrome browser (using Selenium)
	driver = start_browser()

	results = []

	for key, link in pages.items():

		print(f"Working on {key}...")

		# Opens the link to the site.
		driver.get(link)
		sleep(10)
		print("There could be Cloudflare protection. Now you have 10s to deal with it.")

		# Close Cookies Thingy...
		try:
			decline_btn = look_for_ref(driver, '#declineButton', 1)
			decline_btn.click()
			print('Closed Cookies. I will sleep 4s now and wait for full page load.')
			sleep(4)
		except:
			print("No cookies button found, moving on.")


		# Find all classes of links to products
		tiles = driver.find_elements(By.CSS_SELECTOR, '[data-role="offer"]')

		print(len(tiles))

		for tile in tiles:

			########################
			#* Product Info
			########################
			info = look_for_ref(tile, '[data-role="productInformation"]', 0)
			name = get_element_text(info, 'p:first-of-type', 0)

			products = re.split(r'\s*eller\s*|\s*,\s*', name)
			products = [p.strip() for p in products if p.strip()]
			for product in products:
				scraped_data = get_items(tile, info)
				results.append(["Coop", product, *scraped_data, date.today()])

	return results



def start_coop(n_drivers: int, pages: str) -> pd.DataFrame:

	# One-time pass to map out all links that need to be visited.
	contents = scrape(pages)

	# Print the extracted contents
	contents = pd.DataFrame(contents, columns=["Retail", "Name", "Price", "Category", "Img", "Link", "Quantity", "Unit", "Date of Update"])

	mkdir("./static/scraper/processed")
	contents.to_csv("./static/scraper/processed/Coop.csv")
	print("Coop Done!")
	return contents
