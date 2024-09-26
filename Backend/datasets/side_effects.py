import pandas as pd


side_effects = ["Nausea", "Headache", "Dizziness", "Fatigue", "Diarrhea",
    "Constipation", "Rash", "Dry Mouth", "Insomnia", "Weight Gain",
    "Weight Loss", "Increased Heart Rate", "Low Blood Pressure",
    "Muscle Pain", "Joint Pain", "Blurred Vision", "Sweating",
    "Tremors", "Depression", "Anxiety"]


side_effect_ids = list(range(1, 1 + len(side_effects)))

# Create a DataFrame
data = {
    'side_effect_id': side_effect_ids,
    'side_effect': side_effects
}

# Convert to a Pandas DataFrame
df = pd.DataFrame(data)

# Display the DataFrame in tabular format
print(df)

df.to_csv('side_effect.csv', index=False)

print("Data exported to 'side_effect.csv' successfully!")