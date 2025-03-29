import pandas as pd
from modules.silmaasema import start_silmaasema
from utiles.mkdir import mkdir

def main():
    # Assuming start_synsam, start_silmaasema, and start_uni return dataframes
    df_silmaasema = start_silmaasema(5, {"Silmaasema": "https://www.silmaasema.fi/tuotteet/piilolinssit?cgid=piilolinssit&start=0&sz=100"})

    # Combine the dataframes
    combined_df = pd.concat([df_silmaasema], ignore_index=True) # In case there is more, here is where you combine

    # Export to CSV

    mkdir('./static/scraper/export')
    combined_df.to_csv('./static/scraper/export/combined_data.csv', index=False)

    print("Data has been combined and exported to 'combined_data.csv'.")

# Call the main function
if __name__ == "__main__":
    main()
