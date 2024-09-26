import pandas as pd

# Create data for medical condition
medical_condition_names = ["Hypertension",
    "Diabetes",
    "Allergies",
    "Asthma",
    "Arthritis",
    "Depression",
    "Anxiety",
    "Migraine",
    "Cholesterol",
    "Heart Disease",
    "Osteoporosis",
    "Insomnia",
    "Obesity",
    "Thyroid Disorders",
    "Anemia",
    "Gastroesophageal Reflux Disease (GERD)",
    "Influenza",
    "Chronic Obstructive Pulmonary Disease (COPD)",
    "Psoriasis",
    "Epilepsy",
    "HIV/AIDS",
    "Cancer",
    "Tuberculosis",
    "Alzheimer's Disease",
    "Parkinson's Disease",
    "Hepatitis",
    "Kidney Disease",
    "Liver Disease",
    "Stroke",
    "Multiple Sclerosis",
    "Irritable Bowel Syndrome (IBS)",
    "Celiac Disease",
    "Pneumonia",
    "Eczema",
    "Gout",
    "Menopause",
    "Prostate Conditions",
    "Sexually Transmitted Infections (STIs)",
    "Urinary Tract Infection (UTI)",
    "Varicose Veins"]

# Generate medical condition ids starting from 1
medical_condition_ids = list(range(1, 1 + len(medical_condition_names)))

# Create a DataFrame
data = {
    'medical_condition_id': medical_condition_ids,
    'medical_condition_name': medical_condition_names
}

# Convert to a Pandas DataFrame
df = pd.DataFrame(data)

# Display the DataFrame in tabular format
print(df)

df.to_csv('medical_condition_data.csv', index=False)

print("Data exported to 'medical_condition_data.csv' successfully!")
