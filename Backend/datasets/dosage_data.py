import pandas as pd


dosage_names = ["Tablet", "Capsule", "Injection", "Syrup", "Inhaler",
    "Cream", "Ointment", "Gel", "Eye Drops", "Nasal Spray",
    "Patch", "Suppository", "Solution", "Lozenge", "Powder",
    "Foam", "Suspension", "Spray", "Elixir", "Granules"]


dosage_ids = list(range(1, 1 + len(dosage_names)))

# Create a DataFrame
data = {
    'dosage_form_id': dosage_ids,
    'dosage_form_name': dosage_names
}

# Convert to a Pandas DataFrame
df = pd.DataFrame(data)

# Display the DataFrame in tabular format
print(df)

df.to_csv('dosage_forms.csv', index=False)

print("Data exported to 'dosage_forms.csv' successfully!")