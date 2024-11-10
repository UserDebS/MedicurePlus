from supabase import create_client, Client
from datatypes import MedicineData, UserData, AuthData
from service.encryption import strGen, encryption

from dotenv import load_dotenv
from os import getenv
load_dotenv()

class Supabase:
    def __init__(self) -> None:
        self.__key = getenv('SUPABASE_KEY')
        self.__url = getenv('SUPABASE_URL')
        self.__instance : Client = create_client(self.__url, self.__key)
    
    def insertMedicine(self, medicineData : MedicineData) -> dict[str, int]:
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
<<<<<<< HEAD

=======
    
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
    
>>>>>>> 60cb360a762d47704b1bd9259eae9d75be375b61
if __name__ == '__main__':
    s = Supabase()
    
    