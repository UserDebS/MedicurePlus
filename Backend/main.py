from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datatypes import MedicineData,UserData,MedicineDetails
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
        token : str = req.cookies.get('medicure_auth')
        supabase.authBytoken(token)
    except:
        return {
            'status' : 404
        }
@app.post('/login')
def authByUserPass(userdata : UserData, res : Response) -> dict[str, int]:
    try:
         #post userdata to database
    except:
        return{
            'status':400
        }
@app.post('/register')
def register(userdata : UserData, res : Response):
    try:
       #pass 'userdata' to supbase to register user
    except:
        return{
            'status':404
        }
    
@app.post('/medicine')
def getMedicines() -> list[MedicineDetails]:
    try:
        
    except:
        return{
            'status':400
        }

@app.get('/scan')
def scan()->list[str]:
    try:
          #using Med we can get all medicine name
    except:
        return{
            'status':400
        }

@app.get('/home')
def homepage():
    try:
       #rendering homepage
    except:
        return{
            'status':400
        }

@app.get('/home/')
def suggestions(suggestion : str) -> list[str]:


@app.post('/doctor')

@app.post('/consult_doctor')

@app.post('/delivery')


if __name__ == '__main__':
    uvicorn.run(app, port=5500)