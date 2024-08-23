from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
async def root():
    return {
        'written' : 'hello world'
    }

if __name__ == '__main__':
    uvicorn.run(app, port=3000)