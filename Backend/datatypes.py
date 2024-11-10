from pydantic import BaseModel

class MedicineData(BaseModel): # Will be used for uploading medicines
    name : str
    medical_conditions : list[str]
    active_ingredients : list[str]
    dosage_forms : list[str]
    side_effects : list[str]
    brand_names : list[str]

class UserData(BaseModel): # for register purpose
    username : str
    email : str
    password : str

class MedicineDetails(BaseModel): # for medicine card
    name : str
    cost : float
    available : bool
    self_url : str #http://localhost:3000/medicines/{id}

class AuthData(BaseModel): #For authentication purpose
    email : str
    password : str

class ImageData(BaseModel): # I will need the base64 url only
    image : str

class MedicineDetailedData(BaseModel):
    data : MedicineData
    recommendation : list[MedicineDetails]