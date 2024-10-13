from pydantic import BaseModel

class MedicineData(BaseModel):
    name : str
    medical_conditions : list[str]
    active_ingredients : list[str]
    dosage_forms : list[str]
    side_effects : list[str]
    brand_names : list[str]