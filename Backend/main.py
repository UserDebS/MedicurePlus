from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from datatypes import UserData, MedicineData, MedicineDetails
from SupabaseClient import Supabase

import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware, 
    allow_origin=['*'],
    allow_crededentials=True,
    allow_methods=['*'],
    allow_headers=["Access-Control-Allow-Origin", 'Set-Cookie', 'Accept']
)

supabase = Supabase()

@app.get('/login')
def authByToken(req : Request, res : Response) -> dict[str, int]:
    try:
        if(req.cookies.get('medicure_auth') == None):
            return {'status' : 404}
        newtoken = supabase.authByToken(req.cookies.get('medicure_auth'))
        res.set_cookie('medicure_auth', newtoken, max_age = 10 * 24 * 3600000)
        return {
            'status' : 200
        }
    except:
        return {
            'status' : 404
        }
    
@app.post('/login')
def authByUserPass(userdata : UserData, res : Response) -> dict[str, int]:
    try:
         #post userdata to database
         pass
    except:
        return{
            'status':400
        }
    
@app.post('/register')
def register(userdata : UserData, res : Response) -> dict[str, int]:
    try:
       #userdata to supbase to register user
        pass
    except:
        pass
    
@app.get('/medicines')
def getMedicines(req : Request) -> list[MedicineDetails]:
    try:
        pass
    except:
        pass

@app.get('/medicines')
def getSuggestions(suggestion : str) -> list[str]: #Using prefix tree
    try:
        pass
    except:
        pass

@app.get('/medicines')
def getMatchingMedicines(search : str) -> list[MedicineDetails]:
    try:
        pass
    except:
        pass

@app.post('/scan')
def readImageData(img : list[list[list[int, int, int]]]) -> list[MedicineDetails]:
    try:
        #using Med we can get all medicine name
        pass
    except:
        pass
    
@app.post('/scan')
def readTextData(text : str) -> list[MedicineDetails]:
    try:
        pass
    except:
        pass


if __name__ == '__main__':
    uvicorn.run(app, port=5500)