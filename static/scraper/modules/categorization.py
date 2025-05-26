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
############## Kolmogorov Army Sentence Transformers Setup ##########


import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util

# --- Load Data ---
df = pd.read_csv("static/scraper/export/combined_data_translated.csv")
df["Translated Name Cleaned"] = df["Translated Name Cleaned"].astype(str).str.strip(" ,.;:+")
product_names = df["Translated Name Cleaned"].fillna("").tolist()
product_names = [name for name in product_names if name]

# --- Define Labels ---
category_labels = [
    "Chicken Breast", "Chicken Thighs", "Chicken Drumsticks", "Chicken Mixed Cuts", "Pork Chops", "Pork Mince",
    "Beef Mince", "Beef Steak", "Frikadeller", "Liver Pâté", "Cold Cuts", "Ham Slices", "Salami", "Sausage",
    "Fish Fillet", "Fish Cakes", "Smoked Salmon", "Surimi", "Milk", "Cocoa Milk", "Plant Milk", "Yogurt", "Skyr",
    "Cheese Slices", "Cheese Block", "Cream Cheese", "Butter", "Margarine", "Eggs", "Wheat Flour", "Rye Flour",
    "Pasta", "Spaghetti", "Rice", "Couscous", "Bread Crumbs", "Crispbread", "Knækbrød", "Baking Mix", "Bread Loaf",
    "Buns", "Sandwich Bread", "Rye Bread", "Toast Bread", "Tortilla Wraps", "Apples", "Bananas", "Grapes",
    "Tomatoes", "Cucumber", "Potatoes", "Carrots", "Onions", "Garlic", "Lettuce", "Frozen Vegetables", "Juice",
    "Apple Juice", "Orange Juice", "Soda", "Cola", "Energy Drink", "Still Water", "Sparkling Water", "Cocoa Drink",
    "Coffee", "Ground Coffee", "Instant Coffee", "Coffee Beans", "Tea", "Herbal Tea", "Chocolate", "Candy",
    "Biscuits", "Ice Cream", "Magnum", "Waffles", "Licorice", "Baked Beans", "Corn", "Peas", "Pickles", "Jam",
    "Tomato Paste", "Pasta Sauce", "Hummus", "Pizza", "Lasagna", "Ready Meals", "Pasta Salad", "Sandwich Spread",
    "Toilet Paper", "Kitchen Towels", "Dish Soap", "Laundry Detergent", "Shampoo", "Conditioner", "Toothpaste"
]

# --- Load Models ---
model_names = [
    'all-MiniLM-L6-v2',
    'paraphrase-MiniLM-L6-v2',
    'all-distilroberta-v1'
]
models = [SentenceTransformer(name) for name in model_names]

# --- Encode Labels Once ---
label_embeddings_per_model = [model.encode(category_labels, convert_to_tensor=True) for model in models]

# --- Encode Products & Calculate Average Cosine Scores ---
results = []
for product in product_names:
    product_embeddings = [model.encode(product, convert_to_tensor=True) for model in models]

    # Average cosine scores across models
    avg_scores = None
    for emb, label_emb in zip(product_embeddings, label_embeddings_per_model):
        cosine_scores = util.cos_sim(emb, label_emb)
        if avg_scores is None:
            avg_scores = cosine_scores
        else:
            avg_scores += cosine_scores
    avg_scores /= len(models)

    # Get top 3 category indices
    top_scores, top_indices = torch.topk(avg_scores, k=3, dim=1)
    top_scores = top_scores.squeeze().tolist()
    top_indices = top_indices.squeeze().tolist()

    # Handle case when only one score returned (single label tied)
    if not isinstance(top_scores, list):
        top_scores = [top_scores]
        top_indices = [top_indices]

    best_label = category_labels[top_indices[0]]
    results.append({
        "Product": product,
        "Best Category": best_label,
        "Top 1": f"{category_labels[top_indices[0]]} ({top_scores[0]:.2f})",
        "Top 2": f"{category_labels[top_indices[1]]} ({top_scores[1]:.2f})" if len(top_scores) > 1 else "",
        "Top 3": f"{category_labels[top_indices[2]]} ({top_scores[2]:.2f})" if len(top_scores) > 2 else "",
    })

# --- Merge with original data ---
results_df = pd.DataFrame(results)
final_df = df.merge(results_df, how="left", left_on="Translated Name Cleaned", right_on="Product")

# --- Save ---
output_path = "static/scraper/export/combined_data_categorized_ensemble.csv"
final_df.to_csv(output_path, index=False)
print("✅ Done! Saved as 'classified_products_ensemble.csv'")


#############################################################################
############## Sentence Transformers Setup ##########

# import pandas as pd
# import torch
# from sentence_transformers import SentenceTransformer, util

# # Load your CSV
# df = pd.read_csv("static/scraper/export/combined_data_translated.csv")

# # Clean product names
# df["Translated Name Cleaned"] = df["Translated Name Cleaned"].astype(str).str.strip(" ,.;:+")
# product_names = df["Translated Name Cleaned"].fillna("").tolist()
# product_names = [name for name in product_names if name]  # Remove empty

# # Define detailed category labels
# category_labels = [
#     "Chicken Breast", "Chicken Thighs", "Chicken Drumsticks", "Chicken Mixed Cuts", "Pork Chops", "Pork Mince",
#     "Beef Mince", "Beef Steak", "Frikadeller", "Liver Pâté", "Cold Cuts", "Ham Slices", "Salami", "Sausage",
#     "Fish Fillet", "Fish Cakes", "Smoked Salmon", "Surimi", "Milk", "Cocoa Milk", "Plant Milk", "Yogurt", "Skyr",
#     "Cheese Slices", "Cheese Block", "Cream Cheese", "Butter", "Margarine", "Eggs", "Wheat Flour", "Rye Flour",
#     "Pasta", "Spaghetti", "Rice", "Couscous", "Bread Crumbs", "Crispbread", "Knækbrød", "Baking Mix", "Bread Loaf",
#     "Buns", "Sandwich Bread", "Rye Bread", "Toast Bread", "Tortilla Wraps", "Apples", "Bananas", "Grapes",
#     "Tomatoes", "Cucumber", "Potatoes", "Carrots", "Onions", "Garlic", "Lettuce", "Frozen Vegetables", "Juice",
#     "Apple Juice", "Orange Juice", "Soda", "Cola", "Energy Drink", "Still Water", "Sparkling Water", "Cocoa Drink",
#     "Coffee", "Ground Coffee", "Instant Coffee", "Coffee Beans", "Tea", "Herbal Tea", "Chocolate", "Candy",
#     "Biscuits", "Ice Cream", "Magnum", "Waffles", "Licorice", "Baked Beans", "Corn", "Peas", "Pickles", "Jam",
#     "Tomato Paste", "Pasta Sauce", "Hummus", "Pizza", "Lasagna", "Ready Meals", "Pasta Salad", "Sandwich Spread",
#     "Toilet Paper", "Kitchen Towels", "Dish Soap", "Laundry Detergent", "Shampoo", "Conditioner", "Toothpaste"
# ]

# # Load model
# model = SentenceTransformer('all-MiniLM-L6-v2')

# # Encode
# label_embeddings = model.encode(category_labels, convert_to_tensor=True)
# product_embeddings = model.encode(product_names, convert_to_tensor=True)

# # Cosine similarity
# cosine_scores = util.cos_sim(product_embeddings, label_embeddings)
# best_indices = torch.argmax(cosine_scores, dim=1)
# predicted_labels = [category_labels[idx] for idx in best_indices]

# # Assign back
# df["Predicted Category"] = ""
# df.loc[df["Translated Name Cleaned"].isin(product_names), "Predicted Category"] = predicted_labels

# # Save result
# output_path = "static/scraper/export/combined_data_categorized_batch.csv"
# df.to_csv(output_path, index=False)
# print("Done!")


#############################################################################
####### Classification Pipeline Setup ##########


# classifier = pipeline(
#     "zero-shot-classification",
#     model="valhalla/distilbart-mnli-12-1",  # faster!
#     device=-1,
#     batch_size=16 
# )

# labels = [
#     "Chicken Breast",
#     "Chicken Thighs",
#     "Chicken Drumsticks",
#     "Chicken Mixed Cuts",
#     "Pork Chops",
#     "Pork Mince",
#     "Beef Mince",
#     "Beef Steak",
#     "Frikadeller",
#     "Liver Pâté",
#     "Cold Cuts",
#     "Ham Slices",
#     "Salami",
#     "Sausage",
#     "Fish Fillet",
#     "Fish Cakes",
#     "Smoked Salmon",
#     "Surimi",
#     "Milk",
#     "Cocoa Milk",
#     "Plant Milk",
#     "Yogurt",
#     "Skyr",
#     "Cheese Slices",
#     "Cheese Block",
#     "Cream Cheese",
#     "Butter",
#     "Margarine",
#     "Eggs",
#     "Wheat Flour",
#     "Rye Flour",
#     "Pasta",
#     "Spaghetti",
#     "Rice",
#     "Couscous",
#     "Bread Crumbs",
#     "Crispbread",
#     "Knækbrød",
#     "Baking Mix",
#     "Bread Loaf",
#     "Buns",
#     "Sandwich Bread",
#     "Rye Bread",
#     "Toast Bread",
#     "Tortilla Wraps",
#     "Apples",
#     "Bananas",
#     "Grapes",
#     "Tomatoes",
#     "Cucumber",
#     "Potatoes",
#     "Carrots",
#     "Onions",
#     "Garlic",
#     "Lettuce",
#     "Frozen Vegetables",
#     "Juice",
#     "Apple Juice",
#     "Orange Juice",
#     "Soda",
#     "Cola",
#     "Energy Drink",
#     "Still Water",
#     "Sparkling Water",
#     "Cocoa Drink",
#     "Coffee",
#     "Ground Coffee",
#     "Instant Coffee",
#     "Coffee Beans",
#     "Tea",
#     "Herbal Tea",
#     "Chocolate",
#     "Candy",
#     "Biscuits",
#     "Ice Cream",
#     "Magnum",
#     "Waffles",
#     "Licorice",
#     "Baked Beans",
#     "Corn",
#     "Peas",
#     "Pickles",
#     "Jam",
#     "Tomato Paste",
#     "Pasta Sauce",
#     "Hummus",
#     "Pizza",
#     "Lasagna",
#     "Ready Meals",
#     "Pasta Salad",
#     "Sandwich Spread",
#     "Toilet Paper",
#     "Kitchen Towels",
#     "Dish Soap",
#     "Laundry Detergent",
#     "Shampoo",
#     "Conditioner",
#     "Toothpaste"
# ]


# def classify_products_batch(product_names, batch_size=16):
#     categories = []
    
#     # Split into batches
#     for i in tqdm(range(0, len(product_names), batch_size), desc="Classifying in batches"):
#         batch = product_names[i:i+batch_size]
#         results = classifier(
#             batch,
#             candidate_labels=labels,
#             hypothesis_template="This is {}"
#         )
        
#         # When batch has 1 item, results is a dict; when >1 items, results is a list
#         if isinstance(results, dict):
#             best_label = results["labels"][0]
#             categories.append(best_label)
#         else:
#             for res in results:
#                 best_label = res["labels"][0]
#                 categories.append(best_label)
    
#     return categories

# df = pd.read_csv("static/scraper/export/combined_data_translated.csv")

# df["Date of Update"] = df["Date of Update"].combine_first(df["Date of update"])
# df["Translated Name Cleaned"] = df["Translated Name Cleaned"].str.rstrip(" +;")

# sample_df = df.head(40).copy() # Use a smaller sample for testing

# column_to_categorize = "Translated Name Cleaned"

# product_list = [
#     p.strip(" ,.;:") for p in sample_df["Translated Name Cleaned"].fillna("").tolist()
#     if p.strip(" ,.;:")
# ]

# sample_df["Category"] = classify_products_batch(product_list, batch_size=16)

# print(sample_df[["Translated Name Cleaned", "Category"]].to_string(index=False))

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