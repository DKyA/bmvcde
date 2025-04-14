import pandas as pd
from modules.coop_discounts import start_coop
from modules.rema import start_rema
from utiles.mkdir import mkdir

rema_pages = {
         "Bread & Bakery": "https://shop.rema1000.dk/brod-bavinchi",
         "Fruits & Greens": "https://shop.rema1000.dk/frugt-gront",
         "Cooled meats": "https://shop.rema1000.dk/kod-fisk-fjerkrae",
        # "Fridgewares": "https://shop.rema1000.dk/kol",
        # "Cheese": "https://shop.rema1000.dk/ost-mv",
         "Frozen": "https://shop.rema1000.dk/frost",
         "Dairy products": "https://shop.rema1000.dk/mejeri",
         "Colonial Goods": "https://shop.rema1000.dk/kolonial",
    }


def main():

	# Assuming start_synsam, start_silmaasema, and start_uni return dataframes
    df_coop = start_coop(5, {"Coop": "https://365discount.coop.dk/365avis/"})
    df_rema = start_rema(6,rema_pages)
	# Combine the dataframes
    combined_df = pd.concat([df_coop, df_rema], ignore_index=True) # In case there is more, here is where you combine
    


	#
 # Export to CSV
    mkdir('./static/scraper/export')
    combined_df.to_csv('./static/scraper/export/combined_data.csv', index=False)

    print("Data has been combined and exported to 'combined_data.csv'.")
    # Export to CSV

    mkdir('./static/scraper/export')
    combined_df.to_csv('./static/scraper/export/combined_data.csv', index=False)
    
    print("Data has been combined and exported to 'combined_data.csv'.")

# Call the main function

if __name__ == "__main__":
	main()


