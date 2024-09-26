import pandas as pd


active_ingredients_names = ["Acetaminophen", "Ibuprofen", "Amoxicillin", "Cetirizine", "Metformin",
    "Amlodipine", "Simvastatin", "Omeprazole", "Salbutamol", "Prednisone",
    "Hydrochlorothiazide", "Lisinopril", "Atorvastatin", "Levothyroxine",
    "Albuterol", "Doxycycline", "Gabapentin", "Clopidogrel", "Warfarin", "Insulin"]


active_ingredients_ids = list(range(1, 1 + len(active_ingredients_names)))

# Create a DataFrame
data = {
    'active_ingredients_id': active_ingredients_ids,
    'active_ingredients_name': active_ingredients_names
}

# Convert to a Pandas DataFrame
df = pd.DataFrame(data)

# Display the DataFrame in tabular format
print(df)

df.to_csv('active_ingredient_data.csv', index=False)

print("Data exported to 'active_ingredient_data.csv' successfully!")
