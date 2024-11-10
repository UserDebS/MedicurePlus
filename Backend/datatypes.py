from pydantic import BaseModel

class MedicineData(BaseModel):
    name : str
    medical_conditions : list[str]
    active_ingredients : list[str]
    dosage_forms : list[str]
    side_effects : list[str]
    brand_names : list[str]

class UserData(BaseModel):
    username : str
    password : str

class MedicineDetails(BaseModel):
    name : str
    cost : float
    quantity : int
    self_url : str #http://localhost:3000/medicine/{id}
    