from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

if __name__ == '__main__':
    uvicorn.run(app, port=5500)