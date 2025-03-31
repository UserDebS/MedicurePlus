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
    image : str

class UserData(BaseModel): # for register purpose
    username : str
    email : str
    password : str

class MedicineDetails(BaseModel): # for medicine card
    image: str #base64 url
    name : str
    cost : float
    available : bool
    self_url : str #http://localhost:3000/medicines/{id}

class AuthData(BaseModel): #For authentication purpose
    email : str
    password : str

class LocationDetails(BaseModel):
    latitude : float
    longitude : float
    district : str
    state : str
    country : str

class shopOrDeliveryData(BaseModel): #For shop and delivery registrations only
    authdata : AuthData
    locationDetails : LocationDetails

class ImageData(BaseModel): # I will need the base64 url only
    image : str

class MedicineDetailedData(BaseModel):
    data : MedicineData
    recommendation : list[MedicineDetails]

class OrderItem(BaseModel):
    name : str #medicine name
    quantity : int #medicine quantity

class Location(BaseModel):
    latitude : float | int
    longitude : float | int

class Order(BaseModel):
    location : Location
    order_list : list[OrderItem]

class PrevOrderItem(BaseModel):
    name : str
    cost : float
    quantity : int

class PrevOrderModel(BaseModel):
    status : str
    total : float
    placed : str
    orders : list[PrevOrderItem]

class OrderMedicineData(BaseModel):
    medicineName : str
    medicineQuantity : int

class OrderDetails(BaseModel):
    orderId : int
    distance : float
    locationLink : str
    medicineData : list[OrderMedicineData]

class AcceptedOrderDetails(BaseModel):
    orderId : int
    distance : float
    locationLink : str
    medicineData : list[OrderMedicineData]
    orderToken : str