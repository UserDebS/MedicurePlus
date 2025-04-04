from fastapi import FastAPI, Request, Response, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware

import pickle as pkl
import os

from datatypes import AcceptedOrderDetails, ImageData, UserData, MedicineDetails, AuthData, MedicineDetailedData, Order, PrevOrderModel, shopOrDeliveryData, OrderMedicineData, OrderDetails, DeliveryAcceptedOrderDetails
from SupabaseClient import Supabase
from service.trie import Trie
from service.imageClassifier import ImageClassifier

import uvicorn

#%% Init

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'http://localhost:3001'],  # Allows only the origins specified
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, including POST, OPTIONS
    allow_headers=["Access-Control-Allow-Origin", 'Set-Cookie', 'Accept'],  # Allows all headers
)

supabase = Supabase()
pklreader = open(os.path.join(os.path.join(os.path.dirname(__file__), 'model'), 'trie.pkl'), 'rb')
trie : Trie = pkl.load(pklreader)
pklreader.close()
imageClassifier = ImageClassifier(trie=trie)
active_connections : set[WebSocket] = set()

#%% Customer endpoints

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
            raise HTTPException(status_code=404, detail='User does not exist')
        
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
        return supabase.getMedicineWithRecommendationById(id, offset=offset, limit=limit)
    except:
        raise HTTPException(status_code=404, detail='Medicine could not be found')

@app.get('/recommendation/{id}')
def getRecommendationList(id : int, offset : int = 0, limit : int = 20) -> list[MedicineDetails]:
    try :
        return supabase.recommendListById(id, offset=offset, limit=limit)
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
        
        supabase.placeOrder(token=req.cookies.get('medicure_auth'), location=order.location, order_list=order.order_list)

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
    
@app.get('/ordertoken/{orderId}')
async def getOrderToken(orderId : int, req : Request) -> str:
    try:
        if(req.cookies.get('medicure_auth') == None):
            raise HTTPException(status_code=400, detail='Could not get order token')
        return supabase.getOrderToken(req.cookies.get('medicure_auth'), orderId=orderId)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail='Could not get orders')

#%% Shop endpoints

@app.get('/shops/login') #login for shops by cookies
async def authByShopToken(req : Request, res : Response) -> dict[str, int]:
    try:
        if(req.cookies.get('medicure_shop_auth') == None):
            raise HTTPException(status_code=404, detail='Token does not exist')

        status = supabase.authByShopToken(req.cookies.get('medicure_shop_auth'))

        if(status.get('status') == 404):
            raise HTTPException(status_code=404, detail='Token does not exist')
        
        res.set_cookie('medicure_shop_auth', status.get('token'), max_age = 10 * 24 * 3600000, samesite='none', secure=True, httponly=True)

        return {
            'status' : 200
        }
    
    except:
        raise HTTPException(status_code=404, detail='Token does not exist')
    
@app.post('/shops/login')
async def authByShopID(authdata : AuthData,res : Response) -> dict[str, int]:
    try:
        status = supabase.authByShopID(authdata)

        if(status.get('status') == 404):
            raise HTTPException(status_code=404, detail='Shop does not exist')
        
        res.set_cookie('medicure_shop_auth', status.get('token'), max_age = 10 * 24 * 3600000, samesite='none', secure=True, httponly=True)

        return {
            'status' : 200
        }
    except:
        raise HTTPException(status_code=404, detail='Token does not exist')
    
@app.post('/shops/register')
async def shopRegister(shopData : shopOrDeliveryData, res : Response) -> dict[str, int]:
    try:
        status = supabase.shopRegister(shopData=shopData)

        if(status.get('status') == 409):
            raise HTTPException(status_code=409, detail='Account already exists')
          
        res.set_cookie('medicure_shop_auth', status.get('token'), max_age = 10 * 24 * 3600000, samesite='none', secure=True, httponly=True)

        return {
            'status' : 201
        }
    
    except:
        raise HTTPException(status_code=409, detail='Account already exists')

@app.get('/shops/orders/{orderId}')
def getOrderMedicines(orderId : int, req : Request) -> list[OrderMedicineData]:
    try:
        if(req.cookies.get('medicure_shop_auth') == None):
            raise HTTPException(status_code=404, detail='Token does not exist')
        return supabase.getOrderMedicineData(req.cookies.get('medicure_shop_auth'), orderId)
            
    except:
        raise HTTPException(status_code=404, detail='Token or order id does not exist')
    
@app.get('/shops/orders')
def getPendingShopOrders(req : Request) -> list[OrderDetails]:
    try:
        if(req.cookies.get('medicure_shop_auth') == None):
            raise HTTPException(status_code=404, detail='Token does not exist')
        
        return supabase.getPendingShopOrders(req.cookies.get('medicure_shop_auth'))
    except:
        raise HTTPException(status_code=404, detail='Token does not exist')
    
@app.get('/shops/accepted/orders')
def getShopAcceptedOrders(req : Request) -> list[AcceptedOrderDetails]:
    try:
        if(req.cookies.get('medicure_shop_auth') == None):
            raise HTTPException(status_code=404, detail='Token does not exist')
        
        return supabase.getAcceptedOrders(
            token=req.cookies.get('medicure_shop_auth')
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail='Token does not exist')

@app.put('/shops/accepted/orders/{orderId}')
def acceptShopOrders(orderId : int, req : Request) -> dict[str, str | int]:
    try:
        if(req.cookies.get('medicure_shop_auth') == None):
            raise HTTPException(status_code=404, detail='Token does not exist')
        
        return supabase.acceptOrder(
            orderId=orderId,
            token=req.cookies.get('medicure_shop_auth')
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail='Token does not exist')
    
@app.delete('/shops/rejected/orders/{orderId}')
def rejectShopOrders(req : Request, orderId : int) -> dict[str, int]:
    try:
        if(req.cookies.get('medicure_shop_auth') == None):
            raise HTTPException(status_code=404, detail='Token does not exist')
        
        return supabase.rejectOrder(
            orderId=orderId,
            token=req.cookies.get('medicure_shop_auth')
        )
    except:
        raise HTTPException(status_code=404, detail='Token does not exist')
    
@app.patch('/shops/handover')
async def shopHandOver(orderId : int, orderToken : str, req : Request) -> dict[str, int]:
    try:
        if(req.cookies.get('medicure_shop_auth') == None):
            raise HTTPException(status_code=404, detail='Token does not exist')
        
        return supabase.shopHandOver(
            orderId=orderId,
            orderToken=orderToken,
            token=req.cookies.get('medicure_shop_auth')
        )
    except:
        raise HTTPException(status_code=404, detail='Token does not exist')

#%% Delivery endpoints

@app.get('/deliveries/login')
async def authByDeliveryToken(req : Request, res : Response) -> dict[str, str | int]:
    try:
        if(req.cookies.get('medicure_delivery_auth') == None):
            raise HTTPException(status_code=404, detail='Token does not exist')

        status = supabase.authByDeliveryToken(req.cookies.get('medicure_delivery_auth'))

        if(status.get('status') == 404):
            raise HTTPException(status_code=404, detail='Token does not exist')
        
        res.set_cookie('medicure_delivery_auth', status.get('token'), max_age = 10 * 24 * 3600000, samesite='none', secure=True, httponly=True)

        return {
            'status' : 200
        }
    
    except:
        raise HTTPException(status_code=404, detail='Token does not exist')

@app.post('/deliveries/login')
async def authByDeliveryID(authData : AuthData, res : Response) -> dict[str, str | int]:
    try:
        status = supabase.authByDeliveryID(authData)

        if(status.get('status') == 404):
            raise HTTPException(status_code=404, detail='Shop does not exist')
        
        res.set_cookie('medicure_delivery_auth', status.get('token'), max_age = 10 * 24 * 3600000, samesite='none', secure=True, httponly=True)

        return {
            'status' : 200
        }
    except:
        raise HTTPException(status_code=404, detail='Token does not exist')

@app.post('/deliveries/register')
async def deliveryRegister(deliveryData : shopOrDeliveryData, res : Response) -> dict[str, str | int]:
    try:
        status = supabase.deliveryRegister(deliveryData=deliveryData)

        if(status.get('status') == 409):
            raise HTTPException(status_code=409, detail='Account already exists')
          
        res.set_cookie('medicure_delivery_auth', status.get('token'), max_age = 10 * 24 * 3600000, samesite='none', secure=True, httponly=True)

        return {
            'status' : 201
        }
    
    except:
        raise HTTPException(status_code=409, detail='Account already exists')

@app.get('/deliveries/orders')
async def getPendingDeliveryOrders(req : Request) -> list[OrderDetails]:
    try:
        if(req.cookies.get('medicure_delivery_auth') == None):
            raise HTTPException(status_code=404, detail='Token does not exist')
        
        return supabase.getPendingDeliveryOrders(req.cookies.get('medicure_delivery_auth'))
    except:
        raise HTTPException(status_code=404, detail='Token does not exist')
    
@app.get('/deliveries/orders/{shopId}/{orderId}')
async def getDeliveryOrderMedicineData(shopId : int, orderId : int, req : Request) -> list[OrderMedicineData]:
    try:
        if(req.cookies.get('medicure_delivery_auth') == None):
            raise HTTPException(status_code=404, detail='Token does not exist')
        return supabase.getDeliveryOrderMedicineData(req.cookies.get('medicure_delivery_auth'), shopId, orderId)
            
    except:
        raise HTTPException(status_code=404, detail='Token or order id does not exist')

@app.get('/deliveries/accepted/orders')
async def getAcceptedDeliveryOrders(req : Request) -> list[DeliveryAcceptedOrderDetails]:
    try:
        if(req.cookies.get('medicure_delivery_auth') == None):
            raise HTTPException(status_code=404, detail='Token does not exist')
        
        return supabase.getAcceptedDeliveryOrders(
            token=req.cookies.get('medicure_delivery_auth')
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail='Token does not exist')

@app.put('/deliveries/accepted/orders/{orderId}') 
async def acceptDeliveryOrder(orderId : int, req : Request) -> dict[str, int | str]:
    try:
        if(req.cookies.get('medicure_delivery_auth') == None):
            raise HTTPException(status_code=404, detail='Token does not exist')
        
        return supabase.acceptDeliveryOrder(
            orderId=orderId,
            token=req.cookies.get('medicure_delivery_auth')
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail='Token does not exist')

@app.delete('/deliveries/rejected/orders/{orderId}')
async def rejectDeliveryOrder(orderId : int, req : Request) -> dict[str, int]:
    try:
        if(req.cookies.get('medicure_delivery_auth') == None):
            raise HTTPException(status_code=404, detail='Token does not exist')
        
        return supabase.rejectDeliveryOrder(
            orderId=orderId,
            token=req.cookies.get('medicure_delivery_auth')
        )
    except:
        raise HTTPException(status_code=404, detail='Token does not exist')

@app.patch('/deliveries/handover')
async def deliveryHandOver(orderId : int, orderToken : str, req : Request) -> dict[str, int]:
    try:
        if(req.cookies.get('medicure_delivery_auth') == None):
            raise HTTPException(status_code=404, detail='Token does not exist')
        
        return supabase.deliveryHandOver(
            orderId=orderId,
            orderToken=orderToken,
            token=req.cookies.get('medicure_delivery_auth')
        )
    except:
        raise HTTPException(status_code=404, detail='Token does not exist')

@app.patch('/deliveries/signal/{orderId}')
async def setSignal(orderId : int, req : Request) -> dict[str, int]:
    try:
        if(req.cookies.get('medicure_delivery_auth') == None):
            raise HTTPException(status_code=404, detail='Token does not exist')
        
        return supabase.setSignal(
            orderId=orderId,
            token=req.cookies.get('medicure_delivery_auth')
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail='Token does not exist')

#%% Main Function
if __name__ == '__main__':
    uvicorn.run(app, port=5500)