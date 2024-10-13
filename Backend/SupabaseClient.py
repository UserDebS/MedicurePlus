from supabase import create_client, Client
from datatypes import MedicineData
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
            self.__instance.rpc('add_new_medicine', {
                'medicine_data' : medicineData
            }).execute()
            return {
                'status' : 201
            }
        except:
            return {
                'status' : 401
            }
    
    
if __name__ == '__main__':
    s = Supabase()
    
    
