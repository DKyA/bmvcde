import pandas as pd
from modules.coop_discounts import start_coop
from utiles.mkdir import mkdir

def main():

	# Assuming start_synsam, start_silmaasema, and start_uni return dataframes
	df_coop = start_coop(5, {"Coop": "https://365discount.coop.dk/365avis/"})

	# Combine the dataframes
	combined_df = pd.concat([df_coop], ignore_index=True) # In case there is more, here is where you combine

	# Export to CSV
	mkdir('./static/scraper/export')
	combined_df.to_csv('./static/scraper/export/combined_data.csv', index=False)

	print("Data has been combined and exported to 'combined_data.csv'.")

# Call the main function
if __name__ == "__main__":
	main()

