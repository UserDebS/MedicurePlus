from supabase import create_client, Client
from dotenv import load_dotenv
from os import getenv
load_dotenv()
import time as t

class Supabase:
    def __init__(self) -> None:
        self.__key = getenv('SUPABASE_KEY')
        self.__url = getenv('SUPABASE_URL')
        self.__instance : Client = create_client(self.__url, self.__key)
    
    
    
if __name__ == '__main__':
    s = Supabase()
    
    
