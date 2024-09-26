import pandas as pd


brand_names = ["Tylenol", "Advil", "Augmentin", "Zyrtec", "Glucophage",
    "Norvasc", "Zocor", "Prilosec", "Ventolin", "Deltasone",
    "Microzide", "Prinivil", "Lipitor", "Synthroid", "ProAir",
    "Vibramycin", "Neurontin", "Plavix", "Coumadin", "Humalog"]


brand_name_ids = list(range(1, 1 + len(brand_names)))

# Create a DataFrame
data = {
    'brand_name_id': brand_name_ids,
    'brand_name': brand_names
}

# Convert to a Pandas DataFrame
df = pd.DataFrame(data)

# Display the DataFrame in tabular format
print(df)

df.to_csv('brand_names.csv', index=False)

print("Data exported to 'brand_names.csv' successfully!")