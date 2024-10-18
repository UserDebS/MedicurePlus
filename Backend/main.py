from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from datatypes import UserData, MedicineData, MedicineDetails, AuthData
from SupabaseClient import Supabase

import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware, 
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=["Access-Control-Allow-Origin", 'Set-Cookie', 'Accept']
)

supabase = Supabase()

@app.get('/login')
def authByToken(req : Request, res : Response) -> dict[str, int]:
    try:
        if(req.cookies.get('medicure_auth') == None):
            raise HTTPException(status_code=404, detail='Token does not exist')

        status = supabase.authByToken(req.cookies.get('medicure_auth'))

        if(status.get('status') == 404):
            raise HTTPException(status_code=404, detail='Token does not exist')
        
        res.set_cookie('medicure_auth', status.get('token'), max_age = 10 * 24 * 3600000)

        return {
            'status' : 200
        }
    
    except:
        raise HTTPException(status_code=404, detail='Token does not exist')
    
@app.post('/login')
def authByUserPass(authdata : AuthData, res : Response) -> dict[str, int]:
    try:
        status = supabase.authByUserPass(authdata)

        if(status.get('status') == 404):
            raise HTTPException(status_code=404, detail='Token does not exist')
        
        res.set_cookie('medicure_auth', status.get('token'), max_age = 10 * 24 * 3600000)

        return {
            'status' : 200
        }
    except:
        raise HTTPException(status_code=404, detail='Token does not exist')

    
@app.post('/register')
def register(userdata : UserData, res : Response) -> dict[str, int]:
    try:
        status = supabase.register(userdata=userdata)

        if(status.get('status') == 409):
            raise HTTPException(status_code=409, detail='Account already exists')
          
        res.set_cookie('medicure_auth', status.get('token'), max_age = 10 * 24 * 3600000)

        return {
            'status' : 201
        }
    
    except:
        raise HTTPException(status_code=409, detail='Account already exists')

    
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

# @app.post('/scan')
# def readImageData(img : list[list[list[int, int, int]]]) -> list[MedicineDetails]:
#     try:
#         #using Med we can get all medicine name
#         pass
#     except:
#         pass


if __name__ == '__main__':
    uvicorn.run(app, port=5500)