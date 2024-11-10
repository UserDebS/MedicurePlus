from pydantic import BaseModel
from fastapi import UploadFile, File

class MedicineData(BaseModel):
    name : str
    medical_conditions : list[str]
    active_ingredients : list[str]
    dosage_forms : list[str]
    side_effects : list[str]
    brand_names : list[str]

class UserData(BaseModel):
    username : str
<<<<<<< HEAD
=======
    email : str
>>>>>>> 60cb360a762d47704b1bd9259eae9d75be375b61
    password : str

class MedicineDetails(BaseModel):
    name : str
    cost : float
    quantity : int
    self_url : str #http://localhost:3000/medicine/{id}
<<<<<<< HEAD
    
=======

class AuthData(BaseModel): #For authentication purpose
    email : str
    password : str


class ImageData(BaseModel): # I will need the base64 url only
    image : str
>>>>>>> 60cb360a762d47704b1bd9259eae9d75be375b61
