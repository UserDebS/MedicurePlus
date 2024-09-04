from fastapi import FastAPI
from specilizationL import SpecializationTrie, Node

import pickle as pkl
import uvicorn

app = FastAPI()

workingDir = './Backend'
specialization : SpecializationTrie = pkl.load(open('/'.join([workingDir, 'specilizations.pkl']), 'rb'))

@app.get('/')
async def root():
    l : list[str] = specialization.search('sleep')
    return {
        'written' : l
    }

if __name__ == '__main__':
    uvicorn.run(app, port=5500)