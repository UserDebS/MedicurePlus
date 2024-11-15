from fastapi import FastAPI, Request, Response, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pickle as pkl
import os

from datatypes import ImageData, UserData, MedicineDetails, AuthData, MedicineDetailedData, Order, PrevOrderModel
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

@app.get('/login') #done
def authByToken(req : Request, res : Response) -> dict[str, int]:
    try:
        if(req.cookies.get('medicure_auth') == None):
            raise HTTPException(status_code=404, detail='Token does not exist')

        status = supabase.authByToken(req.cookies.get('medicure_auth'))

        if(status.get('status') == 404):
            raise HTTPException(status_code=404, detail='Token does not exist')
        
        res.set_cookie('medicure_auth', status.get('token'), max_age = 10 * 24 * 3600000, samesite='none', secure=True, httponly=True)

        return {
            'status' : 200
        }
    
    except:
        raise HTTPException(status_code=404, detail='Token does not exist')
    
@app.post('/login') #done
def authByUserPass(authdata : AuthData, res : Response) -> dict[str, int]:
    try:
        status = supabase.authByUserPass(authdata)

        if(status.get('status') == 404):
            raise HTTPException(status_code=404, detail='Token does not exist')
        
        res.set_cookie('medicure_auth', status.get('token'), max_age = 10 * 24 * 3600000, samesite='none', secure=True, httponly=True)

        return {
            'status' : 200
        }
    except:
        raise HTTPException(status_code=404, detail='Token does not exist')

    
@app.post('/register') #done
def register(userdata : UserData, res : Response) -> dict[str, int]:
    try:
        status = supabase.register(userdata=userdata)

        if(status.get('status') == 409):
            raise HTTPException(status_code=409, detail='Account already exists')
          
        res.set_cookie('medicure_auth', status.get('token'), max_age = 10 * 24 * 3600000, samesite='none', secure=True, httponly=True)

        return {
            'status' : 201
        }
    
    except:
        raise HTTPException(status_code=409, detail='Account already exists')

    
@app.get('/medicines/') # Get all medicines (Done)
def getMedicines(req : Request, offset : int = 0, limit : int = 20) -> list[MedicineDetails]:
    try:
        if(req.cookies.get('medicure_auth') is None): # plan is to only return list if user is authenticated
            raise HTTPException(status_code=400, detail='Invalid User')
        return supabase.getAllMedicines(offset=offset, limit=limit)
    except:
        return []

@app.get('/medicines/{id}') # Get a specific medicine (Done)
def getMedicineById(id : int, offset : int = 0, limit : int = 20) -> MedicineDetailedData:
    try:
        return supabase.recommendById(id, offset=offset, limit=limit)
    except:
        raise HTTPException(status_code=404, detail='Medicine could not be found')

@app.get('/suggestions/') # Done
async def getSuggestions(search : str) -> list[str]: #Using prefix tree suggestions --
    try:
        return trie.showSimilarities(search)
    except:
        return []

@app.get('/find/') #done
def getSearchedMedicines(search : str, offset : int = 0, limit : int = 20) -> list[MedicineDetails]:# For searching using text
    try:
        return supabase.getSearchedMedicines(search=search, offset=offset, limit=limit) or []
    except:
        return []

@app.post('/upload') #done
async def readImageData(data : ImageData) -> list[MedicineDetails]: # For searching using images -- 
    try:
        return supabase.listToMedicineDetails(imageClassifier.read(data.image))
    except Exception as e:
        print(e)
        return []

@app.post('/order')
async def placeOrder(req : Request, order : Order):
    try: 
        if(req.cookies.get('medicure_auth') == None):
            raise HTTPException(status_code=400, detail='Invalid User')
        supabase.placeOrder(token=req.cookies.get('medicure_auth'), order_list=order.order_list)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Order could not be placed either because of invalid user or some other issue')
    
@app.get('/order')
async def getOrders(req : Request, offset : int = 0, limit : int = 15) -> list[PrevOrderModel]:
    try:
        if(req.cookies.get('medicure_auth') == None):
            raise HTTPException(status_code=400, detail='Could not get orders')
        return supabase.getOrders(req.cookies.get('medicure_auth'), offset=offset, limit=limit)
    except:
        return []

if __name__ == '__main__':
    uvicorn.run(app, port=5500)