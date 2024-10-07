import pandas as pd


active_ingredients_names = ["Acetaminophen", "Ibuprofen", "Amoxicillin", "Cetirizine", "Metformin",
    "Amlodipine", "Simvastatin", "Omeprazole", "Salbutamol", "Prednisone",
    "Hydrochlorothiazide", "Lisinopril", "Atorvastatin", "Levothyroxine",
    "Albuterol", "Doxycycline", "Gabapentin", "Clopidogrel", "Warfarin", "Insulin"]


# Create a DataFrame
data = {
    'medicine_id' : []
}

data.update({
    i : [] for i in active_ingredients_names
})

# Convert to a Pandas DataFrame
df = pd.DataFrame(data)

# Display the DataFrame in tabular format
print(df)

df.to_csv('Backend/datasets/active_ingredient_data.csv', index=False)

print("Data exported to 'active_ingredient_data.csv' successfully!")
