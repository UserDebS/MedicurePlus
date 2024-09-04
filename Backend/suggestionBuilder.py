import pickle as pkl

specializations = [
    'cardiologist',
    'dermatologist',
    'neurologist',
    'orthopedic surgeon',
    'pediatrician',
    'psychiatrist',
    'radiologist',
    'gastroenterologist',
    'endocrinologist',
    'oncologist',
    'urologist',
    'nephrologist',
    'ophthalmologist',
    'rheumatologist',
    'allergist',
    'anesthesiologist',
    'pulmonologist',
    'gynecologist',
    'otolaryngologist',
    'plastic surgeon',
    'hematologist',
    'immunologist',
    'infectious disease specialist',
    'neurosurgeon',
    'obstetrician',
    'pathologist',
    'podiatrist',
    'emergency medicine specialist',
    'sports medicine specialist',
    'geriatrician',
    'family medicine physician',
    'general surgeon',
    'vascular surgeon',
    'thoracic surgeon',
    'hepatologist',
    'intensivist',
    'occupational medicine specialist',
    'pain management specialist',
    'rehabilitation medicine specialist',
    'sleep medicine specialist'
]

medical_conditions = [
    "Hypertension",
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
    "Varicose Veins"
]

active_ingredients = [
    "Acetaminophen", "Ibuprofen", "Amoxicillin", "Cetirizine", "Metformin",
    "Amlodipine", "Simvastatin", "Omeprazole", "Salbutamol", "Prednisone",
    "Hydrochlorothiazide", "Lisinopril", "Atorvastatin", "Levothyroxine",
    "Albuterol", "Doxycycline", "Gabapentin", "Clopidogrel", "Warfarin", "Insulin"
]

dosage_forms = [
    "Tablet", "Capsule", "Injection", "Syrup", "Inhaler",
    "Cream", "Ointment", "Gel", "Eye Drops", "Nasal Spray",
    "Patch", "Suppository", "Solution", "Lozenge", "Powder",
    "Foam", "Suspension", "Spray", "Elixir", "Granules"
]

side_effects = [
    "Nausea", "Headache", "Dizziness", "Fatigue", "Diarrhea",
    "Constipation", "Rash", "Dry Mouth", "Insomnia", "Weight Gain",
    "Weight Loss", "Increased Heart Rate", "Low Blood Pressure",
    "Muscle Pain", "Joint Pain", "Blurred Vision", "Sweating",
    "Tremors", "Depression", "Anxiety"
]

brand_names = [
    "Tylenol", "Advil", "Augmentin", "Zyrtec", "Glucophage",
    "Norvasc", "Zocor", "Prilosec", "Ventolin", "Deltasone",
    "Microzide", "Prinivil", "Lipitor", "Synthroid", "ProAir",
    "Vibramycin", "Neurontin", "Plavix", "Coumadin", "Humalog"
]

medicines = [
    # Pain Relief and Inflammation
    "Aspirin",  # Medical Condition: Pain, Fever; Active Ingredient: Aspirin; Dosage Form: Tablet
    "Ibuprofen",  # Medical Condition: Pain, Inflammation; Active Ingredient: Ibuprofen; Dosage Form: Tablet
    "Diclofenac",  # Medical Condition: Pain, Inflammation; Active Ingredient: Diclofenac Sodium; Dosage Form: Tablet, Gel
    "Naproxen",  # Medical Condition: Pain, Inflammation; Active Ingredient: Naproxen Sodium; Dosage Form: Tablet
    "Celecoxib",  # Medical Condition: Pain, Inflammation; Active Ingredient: Celecoxib; Dosage Form: Capsule
    "Meloxicam",  # Medical Condition: Pain, Inflammation; Active Ingredient: Meloxicam; Dosage Form: Tablet
    "Etodolac",  # Medical Condition: Pain, Inflammation; Active Ingredient: Etodolac; Dosage Form: Tablet
    "Indomethacin",  # Medical Condition: Pain, Inflammation; Active Ingredient: Indomethacin; Dosage Form: Capsule
    "Piroxicam",  # Medical Condition: Pain, Inflammation; Active Ingredient: Piroxicam; Dosage Form: Capsule
    "Ketorolac",  # Medical Condition: Pain; Active Ingredient: Ketorolac Tromethamine; Dosage Form: Tablet, Injection
    "Tramadol",  # Medical Condition: Pain; Active Ingredient: Tramadol Hydrochloride; Dosage Form: Tablet
    "Codeine",  # Medical Condition: Pain; Active Ingredient: Codeine Phosphate; Dosage Form: Tablet
    "Morphine",  # Medical Condition: Pain; Active Ingredient: Morphine Sulfate; Dosage Form: Tablet, Injection
    "Oxycodone",  # Medical Condition: Pain; Active Ingredient: Oxycodone Hydrochloride; Dosage Form: Tablet
    "Hydrocodone",  # Medical Condition: Pain; Active Ingredient: Hydrocodone Bitartrate; Dosage Form: Tablet
    "Fentanyl",  # Medical Condition: Pain; Active Ingredient: Fentanyl; Dosage Form: Patch, Injection
    "Methadone",  # Medical Condition: Pain, Opioid Dependence; Active Ingredient: Methadone Hydrochloride; Dosage Form: Tablet
    "Buprenorphine",  # Medical Condition: Pain, Opioid Dependence; Active Ingredient: Buprenorphine; Dosage Form: Patch, Tablet
    "Naloxone",  # Medical Condition: Opioid Overdose; Active Ingredient: Naloxone Hydrochloride; Dosage Form: Injection, Nasal Spray
    "Naltrexone",  # Medical Condition: Opioid Dependence, Alcohol Dependence; Active Ingredient: Naltrexone Hydrochloride; Dosage Form: Tablet, Injection

    # Cardiovascular Conditions
    "Propranolol",  # Medical Condition: Hypertension, Migraine; Active Ingredient: Propranolol Hydrochloride; Dosage Form: Tablet
    "Atenolol",  # Medical Condition: Hypertension, Migraine; Active Ingredient: Atenolol; Dosage Form: Tablet
    "Verapamil",  # Medical Condition: Hypertension, Migraine; Active Ingredient: Verapamil Hydrochloride; Dosage Form: Tablet
    "Nifedipine",  # Medical Condition: Hypertension, Migraine; Active Ingredient: Nifedipine; Dosage Form: Tablet
    "Diltiazem",  # Medical Condition: Hypertension, Angina; Active Ingredient: Diltiazem Hydrochloride; Dosage Form: Tablet
    "Nitroglycerin",  # Medical Condition: Angina; Active Ingredient: Nitroglycerin; Dosage Form: Tablet, Patch
    "Isosorbide Mononitrate",  # Medical Condition: Angina; Active Ingredient: Isosorbide Mononitrate; Dosage Form: Tablet
    "Digoxin",  # Medical Condition: Heart Failure; Active Ingredient: Digoxin; Dosage Form: Tablet
    "Spironolactone",  # Medical Condition: Heart Failure; Active Ingredient: Spironolactone; Dosage Form: Tablet
    "Eplerenone",  # Medical Condition: Heart Failure; Active Ingredient: Eplerenone; Dosage Form: Tablet
    "Ivabradine",  # Medical Condition: Heart Failure; Active Ingredient: Ivabradine; Dosage Form: Tablet
    "Sacubitril",  # Medical Condition: Heart Failure; Active Ingredient: Sacubitril; Dosage Form: Tablet
    "Valsartan",  # Medical Condition: Hypertension, Heart Failure; Active Ingredient: Valsartan; Dosage Form: Tablet
    "Candesartan",  # Medical Condition: Hypertension, Heart Failure; Active Ingredient: Candesartan; Dosage Form: Tablet
    "Losartan",  # Medical Condition: Hypertension, Heart Failure; Active Ingredient: Losartan; Dosage Form: Tablet
    "Telmisartan",  # Medical Condition: Hypertension; Active Ingredient: Telmisartan; Dosage Form: Tablet
    "Olmesartan",  # Medical Condition: Hypertension; Active Ingredient: Olmesartan; Dosage Form: Tablet
    "Captopril",  # Medical Condition: Hypertension, Heart Failure; Active Ingredient: Captopril; Dosage Form: Tablet
    "Ramipril",  # Medical Condition: Hypertension, Heart Failure; Active Ingredient: Ramipril; Dosage Form: Tablet
    "Perindopril",  # Medical Condition: Hypertension, Heart Failure; Active Ingredient: Perindopril; Dosage Form: Tablet
    "Bisoprolol",  # Medical Condition: Hypertension, Heart Failure; Active Ingredient: Bisoprolol; Dosage Form: Tablet
    "Nebivolol",  # Medical Condition: Hypertension, Heart Failure; Active Ingredient: Nebivolol; Dosage Form: Tablet
    "Carvedilol",  # Medical Condition: Hypertension, Heart Failure; Active Ingredient: Carvedilol; Dosage Form: Tablet
    "Labetalol",  # Medical Condition: Hypertension; Active Ingredient: Labetalol; Dosage Form: Tablet
    "Esmolol",  # Medical Condition: Hypertension; Active Ingredient: Esmolol; Dosage Form: Injection

    # Stroke and Blood Clots
    "Aspirin",  # Medical Condition: Heart Attack Prevention; Active Ingredient: Aspirin; Dosage Form: Tablet
    "Clopidogrel",  # Medical Condition: Heart Attack Prevention; Active Ingredient: Clopidogrel; Dosage Form: Tablet
    "Ticagrelor",  # Medical Condition: Heart Attack Prevention; Active Ingredient: Ticagrelor; Dosage Form: Tablet
    "Prasugrel",  # Medical Condition: Heart Attack Prevention; Active Ingredient: Prasugrel; Dosage Form: Tablet
    "Warfarin",  # Medical Condition: Stroke Prevention; Active Ingredient: Warfarin; Dosage Form: Tablet
    "Dabigatran",  # Medical Condition: Stroke Prevention; Active Ingredient: Dabigatran; Dosage Form: Capsule
    "Apixaban",  # Medical Condition: Stroke Prevention; Active Ingredient: Apixaban; Dosage Form: Tablet
    "Rivaroxaban",  # Medical Condition: Stroke Prevention; Active Ingredient: Rivaroxaban; Dosage Form: Tablet
    "Edoxaban",  # Medical Condition: Stroke Prevention; Active Ingredient: Edoxaban; Dosage Form: Tablet
    "Heparin",  # Medical Condition: Blood Clots; Active Ingredient: Heparin; Dosage Form: Injection
    "Enoxaparin",  # Medical Condition: Blood Clots; Active Ingredient: Enoxaparin; Dosage Form: Injection
    "Fondaparinux",  # Medical Condition: Blood Clots; Active Ingredient: Fondaparinux; Dosage Form: Injection
    "Tinzaparin",  # Medical Condition: Blood Clots; Active Ingredient: Tinzaparin; Dosage Form: Injection
    "Bivalirudin",  # Medical Condition: Blood Clots; Active Ingredient: Bivalirudin; Dosage Form: Injection
    "Alteplase",  # Medical Condition: Stroke; Active Ingredient: Alteplase; Dosage Form: Injection
    "Reteplase",  # Medical Condition: Heart Attack; Active Ingredient: Reteplase; Dosage Form: Injection
    "Tenecteplase",  # Medical Condition: Heart Attack; Active Ingredient: Tenecteplase; Dosage Form: Injection

    # Influenza and Hydration
    "Oseltamivir",  # Medical Condition: Influenza; Active Ingredient: Oseltamivir Phosphate; Dosage Form: Capsule
    "Zanamivir",  # Medical Condition: Influenza; Active Ingredient: Zanamivir; Dosage Form: Inhalation
    "Peramivir",  # Medical Condition: Influenza; Active Ingredient: Peramivir; Dosage Form: Injection
    "Baloxavir",  # Medical Condition: Influenza; Active Ingredient: Baloxavir Marboxil; Dosage Form: Tablet
    "Sodium Chloride",  # Medical Condition: Hydration; Active Ingredient: Sodium Chloride; Dosage Form: Injection
    "Potassium Chloride",  # Medical Condition: Potassium Deficiency; Active Ingredient: Potassium Chloride; Dosage Form: Tablet, Injection
    "Calcium Carbonate",  # Medical Condition: Calcium Deficiency; Active Ingredient: Calcium Carbonate; Dosage Form: Tablet
    "Magnesium Oxide",  # Medical Condition: Magnesium Deficiency; Active Ingredient: Magnesium Oxide; Dosage Form: Tablet
    "Vitamin D",  # Medical Condition: Vitamin D Deficiency; Active Ingredient: Vitamin D; Dosage Form: Tablet, Drop
    "Vitamin B12",  # Medical Condition: Vitamin B12 Deficiency; Active Ingredient: Vitamin B12; Dosage Form: Tablet, Injection
    "Folic Acid",  # Medical Condition: Folic Acid Deficiency; Active Ingredient: Folic Acid; Dosage Form: Tablet
    "Iron Sulfate",  # Medical Condition: Iron Deficiency Anemia; Active Ingredient: Iron Sulfate; Dosage Form: Tablet
    "Vitamin C",  # Medical Condition: Vitamin C Deficiency; Active Ingredient: Vitamin C; Dosage Form: Tablet
    "Calcium Gluconate",  # Medical Condition: Calcium Deficiency; Active Ingredient: Calcium Gluconate; Dosage Form: Injection
    "Vitamin E",  # Medical Condition: Vitamin E Deficiency; Active Ingredient: Vitamin E; Dosage Form: Capsule
    "Vitamin A",  # Medical Condition: Vitamin A Deficiency; Active Ingredient: Vitamin A; Dosage Form: Capsule
]

insertList = []
insertList.extend(specializations)
insertList.extend(medical_conditions)
insertList.extend(active_ingredients)
insertList.extend(dosage_forms)
insertList.extend(side_effects)
insertList.extend(brand_names)
insertList.extend(medicines)
insertList = list(map(lambda x : x.lower(), insertList))


class Node:
    def __init__(self, val : str) -> None:
        self.val = val
        self.children : list[Node] = [None for i in range(41)]
    
class Suggestion:
    def __init__(self) -> None:
        self.__root : Node = Node('')
        self.__suggestion : list[str] = []
        self.__specialchar = {
            ' ' : -1,
            '/' : -2,
            '(' : -3,
            ')' : -4,
            '\'' : -5,
            '0': -6,
            '1': -7,
            '2': -8,
            '3': -9,
            '4': -10,
            '5': -11,
            '6': -12,
            '7': -13,
            '8': -14,
            '9' : -15
        }
    
    def insert(self, val : str, addon : str = ''):
        curr = self.__root
        for i in val:
            if(i in [' ', '/', '(', ')', '\'', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
                if(curr.children[self.__specialchar.get(i)] == None):
                    curr.children[self.__specialchar.get(i)] = Node(addon + i)
                    addon += i
                    curr = curr.children[self.__specialchar.get(i)]
                else:
                    addon += i
                    curr = curr.children[self.__specialchar.get(i)]

            else:
                if(ord(i) - 97 > 26 or ord(i) - 97 < 0):
                    print(i)
                if(curr.children[ord(i) - 97] == None):
                    curr.children[ord(i) - 97] = Node(addon + i)
                    addon += i
                    curr = curr.children[ord(i) - 97]
                
                else: 
                    addon += i
                    curr = curr.children[ord(i) - 97]


    def search(self, val : str) -> list[str]:
        self.__suggestion.clear()
        curr = self.__root
        for i in val:
            if(i in [' ', '/', '(', ')', '\'', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
                curr = curr.children[self.__specialchar.get(i)]
            
            else:
                curr = curr.children[ord(i) - 97]
            
            if(curr == None):
                break

        self.__traversal(curr)
        return self.__suggestion

    def all(self):
        self.__suggestion.clear()
        self.__traversal(self.__root)
        print(self.__suggestion)
        self.__suggestion.clear()

    def __traversal(self, curr : Node):
        if(curr == None):
            return
        if(curr.children.count(None) == 41):
            self.__suggestion.append(curr.val)
        for i in curr.children:
            self.__traversal(i)
        

tree = Suggestion()
for i in insertList:
    tree.insert(i)

with open('./backend/suggestion.pkl', 'wb') as file:
    pkl.dump(tree, file=file)
