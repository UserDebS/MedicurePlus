from SupabaseClient import Supabase
import os
import time as t

medicine_data = {
    "Aspirin": {
        "medical_conditions": ["Pain", "Fever", "Heart Attack Prevention"],
        "active_ingredient": ["Aspirin"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Nausea", "Stomach Irritation", "Bleeding"],
        "brand_names": ["Bayer"]
    },
    "Ibuprofen": {
        "medical_conditions": ["Pain", "Inflammation"],##############
        "active_ingredient": ["Ibuprofen"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Nausea", "Dizziness", "Stomach Pain"],
        "brand_names": ["Advil", "Motrin"]
    },
    "Diclofenac": {
        "medical_conditions": ["Pain", "Inflammation"],
        "active_ingredient": ["Diclofenac Sodium"],
        "dosage_forms": ["Tablet", "Gel"],
        "side_effects": ["Headache", "Dizziness", "Stomach Upset"],
        "brand_names": ["Voltaren", "Cataflam"]
    },
    "Naproxen": {
        "medical_conditions": ["Pain", "Inflammation"],##############
        "active_ingredient": ["Naproxen Sodium"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Indigestion", "Drowsiness", "Headache"],
        "brand_names": ["Aleve"]
    },
    "Celecoxib": {
        "medical_conditions": ["Pain", "Inflammation"],
        "active_ingredient": ["Celecoxib"],
        "dosage_forms": ["Capsule"],
        "side_effects": ["Stomach Pain", "Diarrhea", "Nausea"],
        "brand_names": ["Celebrex"]
    },
    "Meloxicam": {
        "medical_conditions": ["Pain", "Inflammation"],
        "active_ingredient": ["Meloxicam"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Nausea", "Diarrhea", "Headache"],
        "brand_names": ["Mobic"]
    },
    "Tramadol": {
        "medical_conditions": ["Pain"],
        "active_ingredient": ["Tramadol Hydrochloride"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Drowsiness", "Nausea", "Dizziness"],
        "brand_names": ["Ultram"]
    },
    "Fentanyl": {
        "medical_conditions": ["Pain"],
        "active_ingredient": ["Fentanyl"],
        "dosage_forms": ["Patch", "Injection"],
        "side_effects": ["Drowsiness", "Nausea", "Constipation"],
        "brand_names": ["Duragesic"]
    },
    "Propranolol": {
        "medical_conditions": ["Hypertension", "Migraine"],
        "active_ingredient": ["Propranolol Hydrochloride"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Dizziness", "Fatigue", "Cold Extremities"],
        "brand_names": ["Inderal"]
    },
    "Atenolol": {
        "medical_conditions": ["Hypertension", "Migraine"],
        "active_ingredient": ["Atenolol"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Dizziness", "Fatigue", "Slow Heart Rate"],
        "brand_names": ["Tenormin"]
    },
    "Verapamil": {
        "medical_conditions": ["Hypertension", "Migraine"],
        "active_ingredient": ["Verapamil Hydrochloride"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Constipation", "Dizziness", "Fatigue"],
        "brand_names": ["Calan", "Verelan"]
    },
    "Nifedipine": {
        "medical_conditions": ["Hypertension", "Migraine"],
        "active_ingredient": ["Nifedipine"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Swelling", "Dizziness", "Headache"],
        "brand_names": ["Procardia"]
    },
    "Nitroglycerin": {
        "medical_conditions": ["Angina"],
        "active_ingredient": ["Nitroglycerin"],
        "dosage_forms": ["Tablet", "Patch"],
        "side_effects": ["Headache", "Dizziness", "Flushing"],
        "brand_names": ["Nitrostat", "Nitro-Dur"]
    },
    "Clopidogrel": {
        "medical_conditions": ["Heart Attack Prevention"],
        "active_ingredient": ["Clopidogrel"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Bleeding", "Bruising", "Nausea"],
        "brand_names": ["Plavix"]
    },
    "Warfarin": {
        "medical_conditions": ["Stroke Prevention"],
        "active_ingredient": ["Warfarin"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Bleeding", "Bruising", "Nausea"],
        "brand_names": ["Coumadin"]
    },
    "Dabigatran": {
        "medical_conditions": ["Stroke Prevention"],
        "active_ingredient": ["Dabigatran"],
        "dosage_forms": ["Capsule"],
        "side_effects": ["Bleeding", "Stomach Pain", "Indigestion"],
        "brand_names": ["Pradaxa"]
    },
    "Oseltamivir": {
        "medical_conditions": ["Influenza"],
        "active_ingredient": ["Oseltamivir Phosphate"],
        "dosage_forms": ["Capsule"],
        "side_effects": ["Nausea", "Vomiting", "Headache"],
        "brand_names": ["Tamiflu"]
    },
    "Vitamin D": {
        "medical_conditions": ["Vitamin D Deficiency"],
        "active_ingredient": ["Vitamin D"],
        "dosage_forms": ["Tablet", "Drop"],
        "side_effects": ["Nausea", "Weakness", "Constipation"],
        "brand_names": ["Calciferol"]
    },
    "Calcium Carbonate": {
        "medical_conditions": ["Calcium Deficiency"],
        "active_ingredient": ["Calcium Carbonate"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Constipation", "Stomach Upset", "Gas"],
        "brand_names": ["Tums", "Caltrate"]
    }
}

medicine_data.update({
    "Amoxicillin": {
        "medical_conditions": ["Bacterial Infections"],
        "active_ingredient": ["Amoxicillin"],
        "dosage_forms": ["Capsule", "Tablet"],
        "side_effects": ["Diarrhea", "Nausea", "Rash"],
        "brand_names": ["Amoxil"]
    },
    "Azithromycin": {
        "medical_conditions": ["Bacterial Infections"],
        "active_ingredient": ["Azithromycin"],
        "dosage_forms": ["Tablet", "Oral Suspension"],
        "side_effects": ["Diarrhea", "Nausea", "Abdominal Pain"],
        "brand_names": ["Zithromax"]
    },
    "Ciprofloxacin": {
        "medical_conditions": ["Bacterial Infections"],
        "active_ingredient": ["Ciprofloxacin"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Nausea", "Diarrhea", "Dizziness"],
        "brand_names": ["Cipro"]
    },
    "Clindamycin": {
        "medical_conditions": ["Bacterial Infections"],
        "active_ingredient": ["Clindamycin"],
        "dosage_forms": ["Capsule", "Injection"],
        "side_effects": ["Diarrhea", "Nausea", "Rash"],
        "brand_names": ["Cleocin"]
    },
    "Metronidazole": {
        "medical_conditions": ["Bacterial Infections"],
        "active_ingredient": ["Metronidazole"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Nausea", "Headache", "Metallic Taste"],
        "brand_names": ["Flagyl"]
    },
    "Doxycycline": {
        "medical_conditions": ["Bacterial Infections"],
        "active_ingredient": ["Doxycycline"],
        "dosage_forms": ["Capsule"],
        "side_effects": ["Nausea", "Vomiting", "Diarrhea"],
        "brand_names": ["Vibramycin"]
    },
    "Levofloxacin": {
        "medical_conditions": ["Bacterial Infections"],
        "active_ingredient": ["Levofloxacin"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Nausea", "Diarrhea", "Headache"],
        "brand_names": ["Levaquin"]
    },
    "Penicillin": {
        "medical_conditions": ["Bacterial Infections"],
        "active_ingredient": ["Penicillin V Potassium"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Nausea", "Diarrhea", "Rash"],
        "brand_names": ["Pen-Vee K"]
    },
    "Cephalexin": {
        "medical_conditions": ["Bacterial Infections"],
        "active_ingredient": ["Cephalexin"],
        "dosage_forms": ["Capsule"],
        "side_effects": ["Nausea", "Diarrhea", "Rash"],
        "brand_names": ["Keflex"]
    },
    "Fluconazole": {
        "medical_conditions": ["Fungal Infections"],
        "active_ingredient": ["Fluconazole"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Nausea", "Headache", "Abdominal Pain"],
        "brand_names": ["Diflucan"]
    },
    "Ketoconazole": {
        "medical_conditions": ["Fungal Infections"],
        "active_ingredient": ["Ketoconazole"],
        "dosage_forms": ["Tablet", "Cream"],
        "side_effects": ["Nausea", "Headache", "Dizziness"],
        "brand_names": ["Nizoral"]
    },
    "Miconazole": {
        "medical_conditions": ["Fungal Infections"],
        "active_ingredient": ["Miconazole"],
        "dosage_forms": ["Cream"],
        "side_effects": ["Burning", "Itching", "Irritation"],
        "brand_names": ["Monistat"]
    },
    "Clotrimazole": {
        "medical_conditions": ["Fungal Infections"],
        "active_ingredient": ["Clotrimazole"],
        "dosage_forms": ["Cream", "Lozenge"],
        "side_effects": ["Burning", "Itching", "Redness"],
        "brand_names": ["Lotrimin"]
    },
    "Terbinafine": {
        "medical_conditions": ["Fungal Infections"],
        "active_ingredient": ["Terbinafine"],
        "dosage_forms": ["Tablet", "Cream"],
        "side_effects": ["Nausea", "Diarrhea", "Headache"],
        "brand_names": ["Lamisil"]
    },
    "Acyclovir": {
        "medical_conditions": ["Viral Infections"],
        "active_ingredient": ["Acyclovir"],
        "dosage_forms": ["Tablet", "Cream"],
        "side_effects": ["Nausea", "Diarrhea", "Headache"],
        "brand_names": ["Zovirax"]
    },
    "Valacyclovir": {
        "medical_conditions": ["Viral Infections"],
        "active_ingredient": ["Valacyclovir"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Nausea", "Headache", "Dizziness"],
        "brand_names": ["Valtrex"]
    },
    "Ribavirin": {
        "medical_conditions": ["Viral Infections"],
        "active_ingredient": ["Ribavirin"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Nausea", "Fatigue", "Headache"],
        "brand_names": ["Rebetol"]
    },
    "Oseltamivir": {
        "medical_conditions": ["Influenza"],
        "active_ingredient": ["Oseltamivir Phosphate"],
        "dosage_forms": ["Capsule"],
        "side_effects": ["Nausea", "Vomiting", "Headache"],
        "brand_names": ["Tamiflu"]
    },
    "Chloroquine": {
        "medical_conditions": ["Malaria"],
        "active_ingredient": ["Chloroquine"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Nausea", "Diarrhea", "Headache"],
        "brand_names": ["Aralen"]
    },
    "Hydroxychloroquine": {
        "medical_conditions": ["Malaria", "Lupus"],
        "active_ingredient": ["Hydroxychloroquine"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Nausea", "Dizziness", "Headache"],
        "brand_names": ["Plaquenil"]
    }
})
medicine_data.update({
    "Calcium Carbonate": {
        "medical_conditions": ["Calcium Deficiency", "Osteoporosis"],
        "active_ingredient": ["Calcium Carbonate"],
        "dosage_forms": ["Tablet", "Chewable Tablet"],
        "side_effects": ["Constipation", "Gas", "Bloating"],
        "brand_names": ["Tums", "Os-Cal"]
    },
    "Ferrous Sulfate": {
        "medical_conditions": ["Iron Deficiency Anemia"],
        "active_ingredient": ["Ferrous Sulfate"],
        "dosage_forms": ["Tablet", "Liquid"],
        "side_effects": ["Constipation", "Nausea", "Stomach Pain"],
        "brand_names": ["Feosol"]
    },
    "Folic Acid": {
        "medical_conditions": ["Folic Acid Deficiency", "Anemia"],
        "active_ingredient": ["Folic Acid"],
        "dosage_forms": ["Tablet", "Injection"],
        "side_effects": ["Nausea", "Bloating", "Gas"],
        "brand_names": ["Folacin"]
    },
    "Vitamin D3": {
        "medical_conditions": ["Vitamin D Deficiency", "Bone Health"],
        "active_ingredient": ["Cholecalciferol"],
        "dosage_forms": ["Capsule", "Tablet"],
        "side_effects": ["Nausea", "Vomiting", "Constipation"],
        "brand_names": ["Vitamin D3"]
    },
    "Vitamin B12": {
        "medical_conditions": ["Vitamin B12 Deficiency", "Anemia"],
        "active_ingredient": ["Cyanocobalamin"],
        "dosage_forms": ["Tablet", "Injection"],
        "side_effects": ["Diarrhea", "Nausea", "Itching"],
        "brand_names": ["Calomist"]
    },
    "Omega-3 Fatty Acids": {
        "medical_conditions": ["Heart Health", "High Cholesterol"],
        "active_ingredient": ["EPA and DHA"],
        "dosage_forms": ["Capsule", "Liquid"],
        "side_effects": ["Fishy Aftertaste", "Nausea", "Diarrhea"],
        "brand_names": ["Fish Oil"]
    },
    "Glucosamine": {
        "medical_conditions": ["Osteoarthritis"],
        "active_ingredient": ["Glucosamine"],
        "dosage_forms": ["Capsule", "Tablet"],
        "side_effects": ["Nausea", "Diarrhea", "Heartburn"],
        "brand_names": ["Cosamin"]
    },
    "Chondroitin": {
        "medical_conditions": ["Osteoarthritis"],
        "active_ingredient": ["Chondroitin Sulfate"],
        "dosage_forms": ["Capsule", "Tablet"],
        "side_effects": ["Nausea", "Diarrhea", "Abdominal Pain"],
        "brand_names": ["Chondroitin"]
    },
    "Lactobacillus": {
        "medical_conditions": ["Digestive Health"],
        "active_ingredient": ["Lactobacillus"],
        "dosage_forms": ["Capsule", "Powder"],
        "side_effects": ["Gas", "Bloating", "Diarrhea"],
        "brand_names": ["Culturelle"]
    },
    "Probiotics": {
        "medical_conditions": ["Gut Health"],
        "active_ingredient": ["Various Probiotics"],
        "dosage_forms": ["Capsule", "Powder"],
        "side_effects": ["Gas", "Bloating"],
        "brand_names": ["Align"]
    },
    "Aspirin": {
        "medical_conditions": ["Pain", "Inflammation", "Heart Attack Prevention"],
        "active_ingredient": ["Aspirin"],
        "dosage_forms": ["Tablet", "Chewable Tablet"],
        "side_effects": ["Stomach Pain", "Nausea", "Gastrointestinal Bleeding"],
        "brand_names": ["Bayer Aspirin"]
    },
    "Ibuprofen": {
        "medical_conditions": ["Pain", "Inflammation", "Fever"],
        "active_ingredient": ["Ibuprofen"],
        "dosage_forms": ["Tablet", "Liquid"],
        "side_effects": ["Stomach Pain", "Nausea", "Heartburn"],
        "brand_names": ["Advil", "Motrin"]
    },
    "Naproxen": {
        "medical_conditions": ["Pain", "Inflammation"],
        "active_ingredient": ["Naproxen"],
        "dosage_forms": ["Tablet", "Liquid"],
        "side_effects": ["Stomach Pain", "Nausea", "Headache"],
        "brand_names": ["Aleve"]
    },
    "Acetaminophen": {
        "medical_conditions": ["Pain", "Fever"],
        "active_ingredient": ["Acetaminophen"],
        "dosage_forms": ["Tablet", "Liquid"],
        "side_effects": ["Nausea", "Stomach Pain", "Allergic Reactions"],
        "brand_names": ["Tylenol"]
    },
    "Morphine": {
        "medical_conditions": ["Severe Pain"],
        "active_ingredient": ["Morphine"],
        "dosage_forms": ["Tablet", "Injection"],
        "side_effects": ["Drowsiness", "Constipation", "Nausea"],
        "brand_names": ["MS Contin"]
    },
    "Oxycodone": {
        "medical_conditions": ["Severe Pain"],
        "active_ingredient": ["Oxycodone"],
        "dosage_forms": ["Tablet", "Liquid"],
        "side_effects": ["Drowsiness", "Nausea", "Constipation"],
        "brand_names": ["OxyContin"]
    },
    "Hydrocodone": {
        "medical_conditions": ["Severe Pain"],
        "active_ingredient": ["Hydrocodone"],
        "dosage_forms": ["Tablet", "Liquid"],
        "side_effects": ["Drowsiness", "Nausea", "Constipation"],
        "brand_names": ["Vicodin"]
    },
    "Tramadol": {
        "medical_conditions": ["Moderate to Severe Pain"],
        "active_ingredient": ["Tramadol"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Dizziness", "Nausea", "Constipation"],
        "brand_names": ["Ultram"]
    },
    "Gabapentin": {
        "medical_conditions": ["Nerve Pain", "Seizures"],
        "active_ingredient": ["Gabapentin"],
        "dosage_forms": ["Capsule", "Tablet"],
        "side_effects": ["Dizziness", "Drowsiness", "Fatigue"],
        "brand_names": ["Neurontin"]
    },
    "Pregabalin": {
        "medical_conditions": ["Nerve Pain", "Fibromyalgia"],
        "active_ingredient": ["Pregabalin"],
        "dosage_forms": ["Capsule", "Liquid"],
        "side_effects": ["Dizziness", "Drowsiness", "Dry Mouth"],
        "brand_names": ["Lyrica"]
    },
    "Clonazepam": {
        "medical_conditions": ["Anxiety", "Seizures"],
        "active_ingredient": ["Clonazepam"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Drowsiness", "Dizziness", "Fatigue"],
        "brand_names": ["Klonopin"]
    },
    "Diazepam": {
        "medical_conditions": ["Anxiety", "Muscle Spasms"],
        "active_ingredient": ["Diazepam"],
        "dosage_forms": ["Tablet", "Injection"],
        "side_effects": ["Drowsiness", "Fatigue", "Confusion"],
        "brand_names": ["Valium"]
    },
    "Alprazolam": {
        "medical_conditions": ["Anxiety", "Panic Disorder"],
        "active_ingredient": ["Alprazolam"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Drowsiness", "Dizziness", "Fatigue"],
        "brand_names": ["Xanax"]
    },
    "Sertraline": {
        "medical_conditions": ["Depression", "Anxiety"],
        "active_ingredient": ["Sertraline"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Nausea", "Diarrhea", "Insomnia"],
        "brand_names": ["Zoloft"]
    },
    "Fluoxetine": {
        "medical_conditions": ["Depression", "Anxiety"],
        "active_ingredient": ["Fluoxetine"],
        "dosage_forms": ["Capsule", "Tablet"],
        "side_effects": ["Nausea", "Headache", "Insomnia"],
        "brand_names": ["Prozac"]
    },
    "Citalopram": {
        "medical_conditions": ["Depression"],
        "active_ingredient": ["Citalopram"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Nausea", "Dry Mouth", "Somnolence"],
        "brand_names": ["Celexa"]
    },
    "Escitalopram": {
        "medical_conditions": ["Depression", "Anxiety"],
        "active_ingredient": ["Escitalopram"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Nausea", "Fatigue", "Dizziness"],
        "brand_names": ["Lexapro"]
    },
    "Venlafaxine": {
        "medical_conditions": ["Depression", "Anxiety"],
        "active_ingredient": ["Venlafaxine"],
        "dosage_forms": ["Capsule", "Tablet"],
        "side_effects": ["Nausea", "Dry Mouth", "Dizziness"],
        "brand_names": ["Effexor"]
    },
    "Bupropion": {
        "medical_conditions": ["Depression", "Smoking Cessation"],
        "active_ingredient": ["Bupropion"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Insomnia", "Dry Mouth", "Nausea"],
        "brand_names": ["Wellbutrin"]
    },
    "Lithium": {
        "medical_conditions": ["Bipolar Disorder"],
        "active_ingredient": ["Lithium Carbonate"],
        "dosage_forms": ["Tablet", "Capsule"],
        "side_effects": ["Nausea", "Tremors", "Thirst"],
        "brand_names": ["Lithobid"]
    },
    "Aripiprazole": {
        "medical_conditions": ["Schizophrenia", "Bipolar Disorder"],
        "active_ingredient": ["Aripiprazole"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Drowsiness", "Dizziness", "Akathisia"],
        "brand_names": ["Abilify"]
    },
    "Risperidone": {
        "medical_conditions": ["Schizophrenia", "Bipolar Disorder"],
        "active_ingredient": ["Risperidone"],
        "dosage_forms": ["Tablet", "Injection"],
        "side_effects": ["Weight Gain", "Drowsiness", "Tremors"],
        "brand_names": ["Risperdal"]
    },
    "Quetiapine": {
        "medical_conditions": ["Schizophrenia", "Bipolar Disorder"],
        "active_ingredient": ["Quetiapine"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Drowsiness", "Weight Gain", "Dry Mouth"],
        "brand_names": ["Seroquel"]
    },
    "Olanzapine": {
        "medical_conditions": ["Schizophrenia", "Bipolar Disorder"],
        "active_ingredient": ["Olanzapine"],
        "dosage_forms": ["Tablet", "Injection"],
        "side_effects": ["Weight Gain", "Drowsiness", "Increased Appetite"],
        "brand_names": ["Zyprexa"]
    },
    "Metformin": {
        "medical_conditions": ["Type 2 Diabetes"],
        "active_ingredient": ["Metformin"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Nausea", "Diarrhea", "Stomach Upset"],
        "brand_names": ["Glucophage"]
    },
    "Glipizide": {
        "medical_conditions": ["Type 2 Diabetes"],
        "active_ingredient": ["Glipizide"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Nausea", "Dizziness", "Hypoglycemia"],
        "brand_names": ["Glucotrol"]
    },
    "Glyburide": {
        "medical_conditions": ["Type 2 Diabetes"],
        "active_ingredient": ["Glyburide"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Nausea", "Dizziness", "Hypoglycemia"],
        "brand_names": ["Diabeta"]
    },
    "Insulin": {
        "medical_conditions": ["Type 1 and 2 Diabetes"],
        "active_ingredient": ["Insulin"],
        "dosage_forms": ["Injection"],
        "side_effects": ["Hypoglycemia", "Weight Gain"],
        "brand_names": ["Humulin", "Lantus"]
    },
    "Sitagliptin": {
        "medical_conditions": ["Type 2 Diabetes"],
        "active_ingredient": ["Sitagliptin"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Nausea", "Headache", "Dizziness"],
        "brand_names": ["Januvia"]
    },
    "Dapagliflozin": {
        "medical_conditions": ["Type 2 Diabetes"],
        "active_ingredient": ["Dapagliflozin"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Urinary Tract Infections", "Fungal Infections"],
        "brand_names": ["Farxiga"]
    },
    "Canagliflozin": {
        "medical_conditions": ["Type 2 Diabetes"],
        "active_ingredient": ["Canagliflozin"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Urinary Tract Infections", "Fungal Infections"],
        "brand_names": ["Invokana"]
    },
    "Liraglutide": {
        "medical_conditions": ["Type 2 Diabetes"],
        "active_ingredient": ["Liraglutide"],
        "dosage_forms": ["Injection"],
        "side_effects": ["Nausea", "Diarrhea", "Vomiting"],
        "brand_names": ["Victoza"]
    },
    "Pioglitazone": {
        "medical_conditions": ["Type 2 Diabetes"],
        "active_ingredient": ["Pioglitazone"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Weight Gain", "Edema", "Heart Failure"],
        "brand_names": ["Actos"]
    },
    "Levothyroxine": {
        "medical_conditions": ["Hypothyroidism"],
        "active_ingredient": ["Levothyroxine"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Nausea", "Weight Loss", "Increased Appetite"],
        "brand_names": ["Synthroid"]
    },
    "Metoprolol": {
        "medical_conditions": ["Hypertension", "Heart Failure"],
        "active_ingredient": ["Metoprolol"],
        "dosage_forms": ["Tablet", "Injection"],
        "side_effects": ["Dizziness", "Fatigue", "Bradycardia"],
        "brand_names": ["Lopressor"]
    },
    "Amlodipine": {
        "medical_conditions": ["Hypertension", "Angina"],
        "active_ingredient": ["Amlodipine"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Swelling", "Dizziness", "Flushing"],
        "brand_names": ["Norvasc"]
    },
    "Losartan": {
        "medical_conditions": ["Hypertension", "Heart Failure"],
        "active_ingredient": ["Losartan"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Dizziness", "Fatigue", "Cough"],
        "brand_names": ["Cozaar"]
    },
    "Hydrochlorothiazide": {
        "medical_conditions": ["Hypertension", "Edema"],
        "active_ingredient": ["Hydrochlorothiazide"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Dizziness", "Electrolyte Imbalance", "Nausea"],
        "brand_names": ["Microzide"]
    },
    "Atorvastatin": {
        "medical_conditions": ["High Cholesterol"],
        "active_ingredient": ["Atorvastatin"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Muscle Pain", "Liver Damage", "Nausea"],
        "brand_names": ["Lipitor"]
    },
    "Simvastatin": {
        "medical_conditions": ["High Cholesterol"],
        "active_ingredient": ["Simvastatin"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Muscle Pain", "Liver Damage", "Nausea"],
        "brand_names": ["Zocor"]
    },
    "Rosuvastatin": {
        "medical_conditions": ["High Cholesterol"],
        "active_ingredient": ["Rosuvastatin"],
        "dosage_forms": ["Tablet"],
        "side_effects": ["Muscle Pain", "Liver Damage", "Nausea"],
        "brand_names": ["Crestor"]
    }
})

def nameToColumn(text : str) -> str:
    return '_'.join(text.lower().split(' '))


if __name__ == '__main__':
    db = Supabase()
    data = {
        'name' : "Lisinopril",
        'medical_conditions' : ["Hypertension", "Heart Failure"],
        'active_ingredients' : ["Lisinopril"],
        'dosage_forms' : ["Tablet"],
        'side_effects' : ["Cough", "Dizziness", "Fatigue", "Hypotension", "Electrolyte Imbalance"],
        'brand_names' : ["Prinivil", "Zestril"],
    }
    print(db.insertMedicine(data))
    
        

    

    