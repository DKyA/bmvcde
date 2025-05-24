import pandas as pd
import re

def clean_names(df):
    if 'Name' not in df.columns:
        raise ValueError("The DataFrame does not contain a 'Name' column.")

    # Words to remove (case-insensitive, supports optional plural forms or punctuation)
    blacklist_words = [
        r'irmas?',           # irmas or irma
        r'[øo]kologisk(e)?', # økologisk, okologisk, økologiske etc.
        r'[øo]ko\.?',        # øko or oko or øko.
        r'dansk(e)?',        # dansk, danske
        r'fersk'             # fersk
    ]

    # Build a regex pattern to match whole words only
    blacklist_pattern = r'\b(?:' + '|'.join(blacklist_words) + r')\b'

    # Clean the 'Name' column without stripping diacritics
    df['Name Cleaned'] = (
        df['Name']
        .fillna('')
        .str.replace(r'\*$', '', regex=True)                         # remove trailing asterisks
        .str.replace(r'[0-9*/"\'.\-%];', '', regex=True)                # remove digits and symbols
        .str.replace(r'\s+', ' ', regex=True)                       # normalize whitespace
        .str.replace(blacklist_pattern, '', flags=re.IGNORECASE, regex=True)  # remove unwanted words
        .str.strip()
        .str.lower()
    )

    return df

df = pd.read_csv("static/scraper/export/combined_data.csv")
df = clean_names(df)

df.to_csv("static/scraper/export/combined_data_cleaned.csv", index=False)
