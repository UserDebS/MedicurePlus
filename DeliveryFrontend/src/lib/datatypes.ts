export type AuthData = {
    email : string,
    password : string
}

export type LocationDetails = {
    latitude : number
    longitude : number
    district : string
    state : string
    country : string
}

export type shopOrDeliveryData = {
    authdata : AuthData
    locationDetails : LocationDetails
}

export type OrderMedicineData = {
    medicineName : string,
    medicineQuantity : number
}

export type OrderDetails = {
    orderId : number,
    distance : number,
    locationLink : string,
    medicineData : OrderMedicineData[]
}

export enum AuthType{
    ShopRegister = 1,
    ShopLogin,
    DeliveryRegister,
    DeliveryLogin
}