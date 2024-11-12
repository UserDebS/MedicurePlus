from pydantic import BaseModel

class MedicineUploadData(BaseModel):
    name : str
    cost : float
    quantity : int
    medical_conditions : list[str]
    active_ingredients : list[str]
    dosage_forms : list[str]
    side_effects : list[str]
    brand_names : list[str]
    
class MedicineData(BaseModel): # Will be used for getting specific medicine by id
    name : str
    cost : float
    available : bool
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

class OrderItem(BaseModel):
    name : str #medicine name
    quantity : int #medicine quantity

class Order(BaseModel):
    order_list : list[OrderItem]

class PrevOrderItem(BaseModel):
    name : str
    cost : float
    quantity : int

class PrevOrderModel(BaseModel):
    total : float
    placed : str
    orders : list[PrevOrderItem]

