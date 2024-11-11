from fastapi import FastAPI, Request, Response, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pickle as pkl
import os

from datatypes import ImageData, UserData, MedicineDetails, AuthData, MedicineDetailedData
from SupabaseClient import Supabase
from service.trie import Trie
from service.imageClassifier import ImageClassifier

import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],  # Allows only the origins specified
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, including POST, OPTIONS
    allow_headers=["Access-Control-Allow-Origin", 'Set-Cookie', 'Accept'],  # Allows all headers
)

supabase = Supabase()
pklreader = open(os.path.join(os.path.join(os.path.dirname(__file__), 'model'), 'trie.pkl'), 'rb')
trie : Trie = pkl.load(pklreader)
pklreader.close()
imageClassifier = ImageClassifier(trie=trie)

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

    
@app.get('/medicines') # Get all medicines
def getMedicines(req : Request, offset : int = 0, limit : int = 20) -> list[MedicineDetails]:
    try:
        if(req.cookies.get('medicure_auth') is None): # plan is to only return list if user is authenticated
            pass
        return supabase.getAllMedicines(offset=offset, limit=limit)
    except:
        return []

@app.get('/medicines/{id}') # Get a specific medicine
def getMedicineById(id : int, offset : int = 0, limit : int = 20) -> MedicineDetailedData:
    try:
        pass
    except:
        pass

@app.get('/suggestions/')
async def getSuggestions(search : str) -> list[str]: #Using prefix tree suggestions --
    try:
        return trie.showSimilarities(search)
    except:
        return []

@app.get('/find/')
def getSearchedMedicines(search : str, offset : int = 0, limit : int = 20) -> list[MedicineDetails]:# For searching using text
    try:
        return supabase.getSearchedMedicines(search=search, offset=offset, limit=limit) or []
    except:
        return []
    
@app.get('/recommend/{id}')
def getRecommendedMedicines(id : int, limit : int = 20, offset : int = 0) -> list[MedicineDetails]:
    try:
        return supabase.recommendById(id, offset=offset, limit=limit)
    except:
        raise HTTPException(status_code=404, detail='Medicine could not be found')

@app.post('/upload')
async def readImageData(data : ImageData) -> list[str]: # For searching using images -- 
    try:
        return imageClassifier.read(data.image)
    except Exception as e:
        print(e)
        return []


if __name__ == '__main__':
    uvicorn.run(app, port=5500)