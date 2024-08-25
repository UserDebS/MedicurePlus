from supabase import create_client, Client
from dotenv import load_dotenv
from os import getenv
load_dotenv()

class Supabase:
    def __init__(self) -> None:
        self.key = getenv('SUPABASE_KEY')
        self.url = getenv('SUPABASE_URL')
        self.instance : Client = create_client(self.url, self.key)
        self.table = 'hello'
    
    def select(self, query : str = '') -> list:
        return self.instance.table(self.table).select(query).execute().data

    def selectFilter(self, query : str = '', filter : dict[str, any] = {}) -> list:
        return self.instance.table(self.table).select(query).match(filter).execute().data
    
    def changeTable(self, table : str) -> None:
        self.table = table

