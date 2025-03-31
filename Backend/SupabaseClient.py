from supabase import create_client, Client, AClient, acreate_client
from threading import Thread
from dotenv import load_dotenv
from os import getenv

from datatypes import AcceptedOrderDetails, Location, MedicineUploadData, UserData, AuthData, MedicineDetails, MedicineDetailedData, OrderItem, PrevOrderModel, shopOrDeliveryData, OrderMedicineData, OrderDetails

from service.encryption import strGen, encryption, capitalize
from service.listClassifier import listClassifier
from service.imageToBase64 import imageToBase64URL
from service.collectionManager import addDataToDicts, addDataToDict

import json

load_dotenv()

class Supabase:
    def __init__(self) -> None:
        self.__key = getenv('SUPABASE_KEY')
        self.__url = getenv('SUPABASE_URL')
        self.__instance : Client = create_client(self.__url, self.__key)
    
    def insertMedicine(self, medicineData : MedicineUploadData) -> dict[str, int]:
        try:
            data : int = self.__instance.rpc('add_new_medicine', {
                'medicine_data' : medicineData
            }).execute().data
            
            return {
                'status' : 201
            }
        except Exception as e:
            print(e)
            return {
                'status' : 401
            }
    
    def authByToken(self, token : str) -> dict[str, int | str]:
        try:
            data : dict[str, any] = self.__instance.table('users').select('user_id').eq('token', encryption(token)).single().execute().data
            newtoken : str = strGen(20)
            self.__instance.table('users').update({'token' : encryption(newtoken)}).eq('user_id', data.get('user_id')).execute()

            return {
                'status' : 200,
                'token' : newtoken
            }
        except:
            return {
                'status' : 404
            }
        
    def authByUserPass(self, authdata : AuthData) -> dict[str, int | str]:
        try:
            authdata.password = encryption(authdata.password)
            data : dict[str, any] = self.__instance.table('users').select('password, salt').eq('email', authdata.email).single().execute().data

            if(data.get('password') != encryption(encryption(data.get('salt')) + authdata.password)):
                return {'status' : 404}
            
            newtoken : str = strGen(20)
            salt : str = strGen(10)
            newpass = encryption(encryption(salt) + authdata.password)
            self.__instance.table('users').update({
                'password' : newpass,
                'salt' : salt,
                'token' : encryption(newtoken)
            }).eq('email', authdata.email).execute()

            return {
                'status' : 200,
                'token' : newtoken
            }
        except Exception as e:
            print(e)
            return {
                'status' : 404
            }
        
    def register(self, userdata : UserData) -> dict[str, int | str]:
        try:
            newtoken : str = strGen(20)
            salt : str = strGen(10)
            userdata.password = encryption(encryption(salt) + encryption(userdata.password))
            self.__instance.table('users').insert({
                'username' : userdata.username,
                'email' : userdata.email,
                'password' : userdata.password,
                'salt' : salt,
                'token' : encryption(newtoken)
            }).execute()

            return {
                'status' : 201,
                'token' : newtoken
            }
        except:
            return {
                'status' : 409
            }
        
    def getMedicineWithRecommendationById(self, id : int, offset : int, limit : int) -> MedicineDetailedData:
        return {
            'data' : addDataToDict(self.__instance.rpc('get_full_medicine_details', {
                'med_id' : id
             }).single().execute().data['data'], 'image', imageToBase64URL),
            'recommendation' : self.recommendListById(id, offset=offset, limit=limit)
        }
    
    def recommendListById(self, id : int, offset : int, limit : int) -> list[MedicineDetails]:
        data =  self.__instance.table('score_storage').select('med_id1, med_id2').or_(f'med_id1.eq.{id},med_id2.eq.{id}').order('score', desc=True).limit(limit).offset(offset).execute().data
        def check(c : dict[str, int]):
            if(c['med_id1'] == id):
                return c['med_id2']
            else:
                return c['med_id1']
            
        data = list(map(check, data))

        return addDataToDicts(self.__instance.rpc('medicinedtlfromlist', {
            'data' : data
        }).execute().data, 'image', imageToBase64URL)


    def getAllMedicines(self, offset : int, limit : int) -> list[MedicineDetails]:
        try:
            return addDataToDicts(self.__instance.table('medicine_with_details').select('*').limit(limit).offset(offset).execute().data, 'image', imageToBase64URL)
        except:
            return []
    
    def getSearchedMedicines(self, search : str, offset : int, limit : int) -> list[MedicineDetails]:
        try:
            return addDataToDicts(self.__instance.rpc('get_searched_medicines', {
                'search' : search,
                'lmt' : limit,
                'offst' : offset
            }).execute().data, 'image', imageToBase64URL)

        except Exception as e:
            print(e)
            return []

    def listToMedicineDetails(self, med_list : list[str]) -> list[MedicineDetails]:
        try:
            return addDataToDicts(self.__instance.table('medicine_with_details').select('*').in_('name', list(map(capitalize ,med_list))).execute().data, 'image', imageToBase64URL)
            
        except:
            return []

    def placeOrder(self, token : str, location : Location, order_list : list[OrderItem]):
        token = encryption(token)
        self.__instance.rpc('place_order', {
            'token_' : token,
            'location' : {
                'latitude' : location.latitude,
                'longitude' : location.longitude
            },
            'order_arr' : list(map(lambda x: {'name' : x.name, 'quantity' : x.quantity},order_list))
        }).execute()

    def getOrders(self, token : str, offset : int = 0, limit : int = 15) -> list[PrevOrderModel]:
        return listClassifier(data = self.__instance.rpc('get_orders',  {
            'token_' : encryption(token),
            'ofst' : offset,
            'lmt' : limit
        }).execute().data)

    def authByShopToken(self, token : str) -> dict[str, int | str]:
        try:
            data : dict[str, any] = self.__instance.table('shop_pickup').select('id').eq('token', encryption(token)).single().execute().data
            newtoken : str = strGen(20)
            self.__instance.table('shop_pickup').update({'token' : encryption(newtoken)}).eq('id', data.get('id')).execute()

            return {
                'status' : 200,
                'token' : newtoken
            }
        except:
            return {
                'status' : 404
            }
        
    def authByShopID(self, authdata : AuthData) -> dict[str, int | str]:
        try:
            authdata.password = encryption(authdata.password)
            data : dict[str, any] = self.__instance.table('shop_pickup').select('password, salt').eq('email', authdata.email).single().execute().data

            if(data.get('password') != encryption(encryption(data.get('salt')) + authdata.password)):
                return {'status' : 404}
            
            newtoken : str = strGen(20)
            salt : str = strGen(10)
            newpass = encryption(encryption(salt) + authdata.password)
            self.__instance.table('shop_pickup').update({
                'password' : newpass,
                'salt' : salt,
                'token' : encryption(newtoken)
            }).eq('email', authdata.email).execute()

            return {
                'status' : 200,
                'token' : newtoken
            }
        except Exception as e:
            print(e)
            return {
                'status' : 404
            }
        
    def shopRegister(self, shopData : shopOrDeliveryData) -> dict[str, str | int]:
        try: 
            newtoken : str = strGen(20)
            salt : str = strGen(10)
            shopData.authdata.password = encryption(encryption(salt) + encryption(shopData.authdata.password))

            id = self.__instance.rpc("shop_register", {
                '_email' : shopData.authdata.email,
                '_password' : shopData.authdata.password,
                '_salt' : salt,
                '_token' : encryption(newtoken),
                '_latitude' : shopData.locationDetails.latitude,
                '_longitude' : shopData.locationDetails.longitude,
                '_district' : shopData.locationDetails.district,
                '_state' : shopData.locationDetails.state,
                '_country' : shopData.locationDetails.country
            }).execute().data

            def delivery_allocation(id : int):
                try:
                    self.__instance.rpc("shop_to_delivery_allocation", {
                        "_shop_id" : id
                    }).execute()
                except Exception as e:
                    print('Delivery allocation failed\nError : ', e)

            Thread(target=delivery_allocation, args=(id,)).start()

            return {
                'status' : 201,
                'token' : newtoken,
            }

        except Exception as e:
            return {
                'status' : 409,
                'error' : e
            }
        
    def authByDeliveryToken(self, token : str) -> dict[str, int | str]:
        try:
            data : dict[str, any] = self.__instance.table('delivery').select('id').eq('token', encryption(token)).single().execute().data
            newtoken : str = strGen(20)
            self.__instance.table('delivery').update({'token' : encryption(newtoken)}).eq('id', data.get('id')).execute()

            return {
                'status' : 200,
                'token' : newtoken
            }
        except:
            return {
                'status' : 404
            }
        
    def authByDeliveryID(self, authdata : AuthData) -> dict[str, int | str]:
        try:
            authdata.password = encryption(authdata.password)
            data : dict[str, any] = self.__instance.table('delivery').select('password, salt').eq('email', authdata.email).single().execute().data

            if(data.get('password') != encryption(encryption(data.get('salt')) + authdata.password)):
                return {'status' : 404}
            
            newtoken : str = strGen(20)
            salt : str = strGen(10)
            newpass = encryption(encryption(salt) + authdata.password)
            self.__instance.table('delivery').update({
                'password' : newpass,
                'salt' : salt,
                'token' : encryption(newtoken)
            }).eq('email', authdata.email).execute()

            return {
                'status' : 200,
                'token' : newtoken
            }
        except Exception as e:
            print(e)
            return {
                'status' : 404
            }
        
    def deliveryRegister(self, deliveryData : shopOrDeliveryData) -> dict[str, int | str]:
        try: 
            newtoken : str = strGen(20)
            salt : str = strGen(10)
            deliveryData.authdata.password = encryption(encryption(salt) + encryption(deliveryData.authdata.password))

            id = self.__instance.rpc("delivery_register", {
                '_email' : deliveryData.authdata.email,
                '_password' : deliveryData.authdata.password,
                '_salt' : salt,
                '_token' : encryption(newtoken),
                '_latitude' : deliveryData.locationDetails.latitude,
                '_longitude' : deliveryData.locationDetails.longitude,
                '_district' : deliveryData.locationDetails.district,
                '_state' : deliveryData.locationDetails.state,
                '_country' : deliveryData.locationDetails.country
            }).execute().data

            def shop_allocation(id : int):
                try:
                    self.__instance.rpc("delivery_to_shop_allocation", {
                        "_delivery_id" : id
                    }).execute()
                except Exception as e:
                    print('Delivery allocation failed\nError : ', e)

            Thread(target=shop_allocation, args=(id,)).start()

            return {
                'status' : 201,
                'token' : newtoken,
            }

        except Exception as e:
            return {
                'status' : 409,
                'error' : e
            }
        
    def getOrderMedicineData(self, token : str, orderId : int) -> list[OrderMedicineData]:
        return list(map(
            lambda x: OrderMedicineData(**{
                'medicineName' : x['medicine_name'],
                'medicineQuantity' : x['medicine_quantity']
            }),
            self.__instance.rpc(
            'getordermedicinedata',
            {
                '_token' : encryption(token),
                '_order_id' : orderId
            }
        ).execute().data))
    
    def getPendingShopOrders(self, token : str) -> list[OrderDetails]:
        return list(map(
            lambda x: OrderDetails(**{
                'orderId' : x['_order_id'],
                'distance' : x['_distance'],
                'locationLink' : x['_link'],
                'medicineData' : json.loads(x['_medicine_data'])
            }),
            self.__instance.rpc(
                'getpendingshoporders',
                {
                    '_token' : encryption(token)
                }
            ).execute().data
        ))
    
    def getAcceptedOrders(self, token : str) -> list[AcceptedOrderDetails]:
        return list(map(
            lambda x: AcceptedOrderDetails(**{
                'orderId' : x['_order_id'],
                'distance' : x['_distance'],
                'locationLink' : x['_link'],
                'medicineData' : json.loads(x['_medicine_data']),
                'orderToken' : x['_order_token']
            }),
            self.__instance.rpc(
            'get_accepted_orders',
            params={
                "_token" : encryption(token)
            }
        ).execute().data))

    def acceptOrder(self, orderId : int, token : str) -> dict[str, int | str]:
        try:
            generatedToken : str = strGen(6)

            self.__instance.rpc(
                'accept_order_by_id',
                params={
                    '_order_id' : orderId,
                    '_token' : encryption(token),
                    '_generated_token' : generatedToken
                }
            ).execute()

            return {
                'status' : 200,
                'order_token' : generatedToken
            }
        except Exception as e:
            print(e)
            raise e

    def rejectOrder(self, orderId : int, token : str) -> dict[str, int]:
        try:
            self.__instance.rpc(
                'reject_order_by_id',
                params={
                    '_order_id' : orderId,
                    '_token' : encryption(token)
                }
            ).execute()

            return {
                'status' : 200
            }
        except Exception as e:
            print(e)
            raise Exception('Something went wrong')
        
    def getPendingDeliveryOrders(self, token : str) -> list[OrderDetails]:
        return list(map(
            lambda x: OrderDetails(**{
                'orderId' : x['_order_id'],
                'distance' : x['_distance'],
                'locationLink' : x['_link'],
                'medicineData' : json.loads(x['_medicine_data'])
            }),
            self.__instance.rpc(
                'get_pending_delivery_orders',
                {
                    '_token' : encryption(token)
                }
            ).execute().data
        ))

    def getDeliveryOrderMedicineData(self, token : str, orderId : int) -> list[OrderMedicineData]:
        return list(map(
            lambda x: OrderMedicineData(**{
                'medicineName' : x['medicine_name'],
                'medicineQuantity' : x['medicine_quantity']
            }),
            self.__instance.rpc(
            'get_delivery_order_medicine_data',
            {
                '_token' : encryption(token),
                '_order_id' : orderId
            }
        ).execute().data))

    def getAcceptedDeliveryOrders(self, token : str) -> list[AcceptedOrderDetails]:
        return list(map(
            lambda x: AcceptedOrderDetails(**{
                'orderId' : x['_order_id'],
                'distance' : x['_distance'],
                'locationLink' : x['_link'],
                'medicineData' : json.loads(x['_medicine_data']),
                'orderToken' : x['_order_token']
            }),
            self.__instance.rpc(
            'get_accepted_delivery_orders',
            params={
                "_token" : encryption(token)
            }
        ).execute().data))

    def acceptDeliveryOrder(self, token : str, orderId : int) -> dict[str, int | str]:
        try:
            generatedToken : str = strGen(6)

            self.__instance.rpc(
                'accept_delivery_order_by_id',
                params={
                    '_order_id' : orderId,
                    '_token' : encryption(token),
                    '_generated_token' : generatedToken
                }
            ).execute()

            return {
                'status' : 200,
                'order_token' : generatedToken
            }
        except Exception as e:
            print(e)
            raise e

    def rejectDeliveryOrder(self, token : str, orderId : int) -> dict[str, int]:
        try:
            self.__instance.rpc(
                'reject_delivery_order_by_id',
                params={
                    '_order_id' : orderId,
                    '_token' : encryption(token)
                }
            ).execute()

            return {
                'status' : 200
            }
        except Exception as e:
            print(e)
            raise Exception('Something went wrong')

if __name__ == '__main__': # plan is to fetch the entire data like brands etc using joins and such I am done for today, see you tomorrow :) DS
    s = Supabase()
    print(s.getPendingShopOrders(
        token='·}ªr¯vE¦ªxw¥qr',
    ))

    
    