import pandas as pd
from modules.coop_discounts import start_coop
from modules.rema import start_rema
from utiles.mkdir import mkdir
from modules.cleaner import clean_names

rema_pages = {
        #  "Bread & Bakery": "https://shop.rema1000.dk/brod-bavinchi",
        #  "Fruits & Greens": "https://shop.rema1000.dk/frugt-gront",
        #  "Easy Meals": "https://shop.rema1000.dk/nemt-hurtigt",
        #  "meat[lol]": "https://shop.rema1000.dk/kod-fisk-fjerkrae",
        #  "Fridgewares": "https://shop.rema1000.dk/kol",
        #  "Cheese": "https://shop.rema1000.dk/ost-mv",
         "Frozen": "https://shop.rema1000.dk/frost"#,
        #  "Dairy products": "https://shop.rema1000.dk/mejeri",
        #  "Colonial Goods": "https://shop.rema1000.dk/kolonial",
        #  "Beverages": "https://shop.rema1000.dk/drikkevarer",
        # "Household": "https://shop.rema1000.dk/husholdning",
        # "Toddlers & children": "https://shop.rema1000.dk/baby-og-smaborn",
        # "Personal Care": "https://shop.rema1000.dk/personlig-pleje",
        #  "Sweets & Snacks": "https://shop.rema1000.dk/slik",
        # "Kiosk": "https://shop.rema1000.dk/kiosk",
    }


def main():

    # df_coop = start_coop(5, {"Coop": "https://365discount.coop.dk/365avis/"})
    df_rema = start_rema(11,rema_pages)
	# Combine the dataframes
    combined_df = pd.concat(
        [
            # df_coop,
            df_rema
        ],
        ignore_index=True
    )

    combined_df = clean_names(combined_df)

    # Export to CSV
    mkdir('./static/scraper/export')
    combined_df.to_csv('./static/scraper/export/combined_data_frozen_rema.csv', index=False)
    print("Data has been combined and exported to 'combined_data_frozen_rema.csv'.")

# Call the main function

if __name__ == "__main__":
	main()
