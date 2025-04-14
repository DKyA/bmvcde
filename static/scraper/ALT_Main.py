import pandas as pd
from modules.rema import start_rema
from utiles.mkdir import mkdir


def ALT_main():
    
    # Assuming start_synsam, start_silmaasema, and start_uni return dataframes
    #df_silmaasema = start_silmaasema(5, {"Silmaasema": "https://www.silmaasema.fi/tuotteet/piilolinssit?cgid=piilolinssit&start=0&sz=100"})
   
    rema_pages = {
         "Brød og bageri": "https://shop.rema1000.dk/brod-bavinchi",
         "Frugt og grønt": "https://shop.rema1000.dk/frugt-gront",
        
    }
    
    df_rema = start_rema(2,rema_pages)
    # Combine the dataframes
    combined_df = pd.concat([df_rema], ignore_index=True) # In case there is more, here is where you combine

    # Export to CSV

    mkdir('./static/scraper/export')
    combined_df.to_csv('./static/scraper/export/combined_data.csv', index=False)
    
    print("Data has been combined and exported to 'combined_data.csv'.")

# Call the main function
if __name__ == "__ALT_main__":
    ALT_main()