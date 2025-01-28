from supabase import create_client, Client
from datatypes import MedicineUploadData, UserData, AuthData, MedicineDetails, MedicineDetailedData, OrderItem, PrevOrderModel
from service.encryption import strGen, encryption, capitalize
from service.listClassifier import listClassifier
from service.imageToBase64 import imageToBase64URL
from service.collectionManager import addDataToDicts, addDataToDict

from dotenv import load_dotenv
from os import getenv
import sys

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

    def placeOrder(self, token : str, order_list : list[OrderItem]):
        token = encryption(token)
        self.__instance.rpc('place_order', {
            'token_' : token,
            'order_arr' : list(map(lambda x: {'name' : x.name, 'quantity' : x.quantity},order_list))
        }).execute()

    def getOrders(self, token : str, offset : int = 0, limit : int = 15) -> list[PrevOrderModel]:
        return listClassifier(data = self.__instance.rpc('get_orders',  {
            'token_' : encryption(token),
            'ofst' : offset,
            'lmt' : limit
        }).execute().data)




if __name__ == '__main__': # plan is to fetch the entire data like brands etc using joins and such I am done for today, see you tomorrow :) DS
    s = Supabase()
    print(s.recommendListById(116, 0, 5))

    
    