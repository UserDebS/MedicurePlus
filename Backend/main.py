from fastapi import FastAPI
from suggestionBuilder import Suggestion, Node

import pickle as pkl
import uvicorn

app = FastAPI()

workingDir = './Backend'
suggest : Suggestion = pkl.load(open('/'.join([workingDir, 'suggestion.pkl']), 'rb'))

@app.get('/')
async def root():
    return {
        'written' : "hello"
    }

@app.get('/suggestion/{suggestion}')
async def searchSuggestion(suggestion : str) -> list[str]:
    return suggest.search(suggestion)


if __name__ == '__main__':
    uvicorn.run(app, port=5500)