from supabase import create_client, Client
from dotenv import load_dotenv
from os import getenv
load_dotenv()
import time as t

class Supabase:
    def __init__(self) -> None:
        self.__key ='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJidnhtamdpenFydG5jbnV6Y3FwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU0MzQwMTgsImV4cCI6MjA0MTAxMDAxOH0.TTkb7NVAUhV7xrnLsiCeGo-UqArncj1VeyBfgXwCIvQ' #getenv('SUPABASE_KEY')
        self.__url = 'medicure@2024'#getenv('SUPABASE_URL')
        self.__instance : Client = create_client(self.__url, self.__key)
    
    
    
    
    
if __name__ == '__main__':
    s = Supabase()
    
    
