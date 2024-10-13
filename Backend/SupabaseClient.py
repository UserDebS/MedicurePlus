from supabase import create_client, Client
from datatypes import MedicineData
from dotenv import load_dotenv
from os import getenv
load_dotenv()

class Supabase:
    def __init__(self) -> None:
        self.__key ='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJidnhtamdpenFydG5jbnV6Y3FwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU0MzQwMTgsImV4cCI6MjA0MTAxMDAxOH0.TTkb7NVAUhV7xrnLsiCeGo-UqArncj1VeyBfgXwCIvQ' #getenv('SUPABASE_KEY')
        self.__url = 'medicure@2024'#getenv('SUPABASE_URL')
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
    
    
