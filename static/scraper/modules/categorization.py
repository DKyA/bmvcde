from transformers import pipeline
import pandas as pd
from tqdm import tqdm

########## Translation Pipeline Setup ##########

# # Load your data
# df = pd.read_csv("static/scraper/export/combined_data"
# ""
# ".csv")

# # Set up the translation pipeline
# translator = pipeline("translation", model="Helsinki-NLP/opus-mt-da-en", max_length=100)

# # Enable progress bar
# tqdm.pandas()

# # Translate function
# def translate_product(name):
#     try:
#         translation = translator(name)[0]['translation_text']
#         return translation
#     except Exception as e:
#         print(f"Translation error on '{name}': {e}")
#         return name  # fallback to original

# # Apply translation only to "Name Cleaned" column
# df["Translated Name Cleaned"] = df["Name Cleaned"].progress_apply(translate_product)

# # Save the result
# df.to_csv("static/scraper/export/combined_data_translated.csv", index=False)

#############################################################################
####### Classification Pipeline Setup ##########


classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli", 
    device=-1, # If you have Nvidia GPU, set to 0 (I dont)
    batch_size=16
)

labels = [
"Bread", "Buns & Rolls", "Pastries", 'Cakes', "Cookies & Biscuits", "Flatbreads", "Toast",


]

def classify_products_batch(product_names, batch_size=16):
    categories = []
    
    # Split into batches
    for i in tqdm(range(0, len(product_names), batch_size), desc="Classifying in batches"):
        batch = product_names[i:i+batch_size]
        results = classifier(
            batch,
            candidate_labels=labels,
            hypothesis_template="This product belongs to the {} category."
        )
        
        # When batch has 1 item, results is a dict; when >1 items, results is a list
        if isinstance(results, dict):
            best_label = results["labels"][0]
            categories.append(best_label)
        else:
            for res in results:
                best_label = res["labels"][0]
                categories.append(best_label)
    
    return categories

df = pd.read_csv("static/scraper/export/combined_data_translated.csv")
sample_df = df.head(32).copy()

column_to_categorize = "Translated Name Cleaned"

product_list = sample_df[column_to_categorize].fillna("").tolist()

sample_df["Category"] = classify_products_batch(product_list, batch_size=16)

print(sample_df[["Translated Name Cleaned", "Category"]].to_string(index=False))

# output_path = "static/scraper/export/combined_data_categorized_batch.csv"
# df.to_csv(output_path, index=False)


##############################################################################################


# import pandas as pd
# from transformers import pipeline

# # Load an instruct-tuned model
# pipe = pipeline("text2text-generation", model="google/flan-t5-base") 

# def hf_generalize_name(name):
#     # prompt = f"Help me translate the name of this grocery from Danish. What is '{name}'? Generalize it to a more common name."
#     prompt = (
#         f"You are a grocery classification expert. "
#         f"Generalize the following product to a common grocery type. "
#         f"Use only 1 or 2 English words. If unsure, answer 'Other'. "
#         f"Product: '{name}'\nGeneral category:"
#     )    
#     result = pipe(prompt, max_new_tokens=20)[0]["generated_text"]
#     return result.strip()

# # Load data
# df = pd.read_csv("static/scraper/export/combined_data_translated.csv")

# # Optional: limit to a sample for testing
# sample_df = df.head(10).copy()

# # Apply the generalization function
# # tqdm.pandas()
# sample_df['Generalized Name'] = sample_df['Translated Name Cleaned'].apply(hf_generalize_name)

# # Print results
# print(sample_df[['Translated Name Cleaned', 'Generalized Name']].to_string(index=False))





####################################################################################################
# # Load Rema
# rema_df = pd.read_csv("static/scraper/processed/Rema.csv")

# # Frequency count
# category_counts = rema_df['Category'].value_counts()

# # Define grouping map
# category_groups = {
#     "BRØD": ["BAGUETTE", "BOLLER", "BRØD", "RUGBRØD", "FLUTES", "TOAST", "PITA"],
#     "DRIKKEVARER": ["SODAVAND", "SMOOTHIES", "SAFT", "JUICE", "VAND", "ENERGIDRIK"],
#     "VIN & SPIRITUS": ["RØDVIN", "HVIDVIN", "ROSEVIN", "SPIRITUS", "CIDER"],
#     "ØL": ["ØL", "SPECIAL ØL"],
#     "MEJERI": ["YOGHURT", "FLØDE", "OST", "SMØR", "CREME", "SKYR", "MÆLK", "DESSERT"],
#     "KØD & PÅLÆG": ["KØD", "PÅLÆG", "KYLLING", "BACON", "KALKUN", "HAMBURGERRYG"],
#     "FRUGT & GRØNT": ["BANAN", "GRØNTSAGER", "FRUGT", "BLOMMER", "KIWI", "GULEROD", "ÆBLE", "CITRON"],
#     "SNACKS & SLIK": ["SNACK", "SLIK", "CHIPS", "CHOKOLADE", "LAKRIDS", "KIKS"],
#     "BAGERI": ["BAGER", "BAGERI", "KAGE", "KANEL", "WIENERBRØD"],
#     "HUSHOLDNING": ["RENGØRING", "OPVASK", "TOILETPAPIR", "VASKEMIDDEL", "HÅNDSÆBE", "DEO"],
#     "FROST": ["FROSNE", "FROST", "IS"],
#     "PLANTEBASERET": ["PLANTEBASERET"],
#     "DÅSEMAD": ["TUN", "DÅSE", "MAJS", "KIKÆRTER", "BØNNER"],
#     "KONDITORI": ["KAGE", "BAGERI", "DESSERT"]
# }

# def map_category(original_cat):
#     original = original_cat.upper()
#     for new_cat, keywords in category_groups.items():
#         if any(word in original for word in keywords):
#             return new_cat
#     return original_cat if category_counts[original_cat] >= 5 else "ANDET"

# # Apply mapping
# rema_df['Mapped Category'] = rema_df['Category'].apply(map_category)

# # Save new version
# rema_df.to_csv("static/scraper/processed/Rema_Cleaned.csv", index=False)


# Install required packages (uncomment in Colab)

# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.pipeline import Pipeline
# from sklearn.compose import ColumnTransformer
# from sklearn.preprocessing import StandardScaler

# def labelize(train, test):

# 	# Features and label
# 	X_train = train[['Name', 'Price']]
# 	y_train = train['Category']

# 	X_test = test[['Name', 'Price']]

# 	# Preprocessing:
# 	preprocessor = ColumnTransformer(transformers=[
# 		('text', TfidfVectorizer(ngram_range=(1, 2)), 'Name'),
# 		('num', StandardScaler(), ['Price'])
# 	])

# 	# Full pipeline
# 	model = Pipeline(steps=[
# 		('preprocess', preprocessor),
# 		('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
# 	])

# 	# Train
# 	model.fit(X_train, y_train)

# 	# Predict
# 	y_pred = model.predict(X_test)

# 	# Add predictions to the test DataFrame
# 	test_with_predictions = test.copy()
# 	test_with_predictions['Predicted Category'] = y_pred

# 	# Display selected columns
# 	print(test_with_predictions[['Name', 'Price', 'Predicted Category']].to_string(index=False))

# 	# Optional: save to file for manual checking
# 	test_with_predictions.to_csv("Coop_with_predictions.csv", index=False)

# 	return test_with_predictions

# df = pd.read_csv("static/scraper/processed/Rema.csv")
# df_test = pd.read_csv("static/scraper/processed/Coop.csv")

# # Clean Rema names
# df['Name'] = df['Name'].str.strip().str.strip('"').str.strip("'")

# # Clean Coop names
# df_test['Name'] = df_test['Name'].str.replace(r'\*$', '', regex=True).str.strip()


# labelize(df, df_test)