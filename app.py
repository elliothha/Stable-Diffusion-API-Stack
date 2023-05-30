import json
import requests

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

def returnPrediction(pos, neg):
    with open('openapi.json') as file:
        json_data = json.load(file)

    url = 'https://api.ai8pool.com/v1/predictions'

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer jg1x2E_qmXDJfcVR.Z/VSjP8-eOhm"
    }

    payload = {
        "prompt": pos,
        "negativePrompt": neg,
        "modelId": "1",
        "height": 512,
        "width": 512,
        "numInferenceSteps": 55,
        # "guidanceScale": 7.5,
        # "scheduler": "DDIM",
        "numImages": 1,
        "scale": "x2"
    }

    response = requests.post(url=url, headers=headers, json=payload)
    print(f"Response Code: {response.status_code}")
    
    data = response.json()

    return data

app = FastAPI()
templates = Jinja2Templates(directory='templates')

app.mount('/static', StaticFiles(directory='static'), name='static')

class FormData(BaseModel):
    positive_input: str
    negative_input: str

@app.get('/')
async def form(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})

@app.post('/process_form')
async def process_form(request: Request, form_data: FormData = Form(...)):
    pos = form_data.positive_input
    neg = form_data.negative_input
    if not pos:
        pos = " "
    if not neg:
        neg = " "
    print(pos)
    print(neg)

    data = returnPrediction(pos=pos, neg=neg)
    url = data['output']['urls'][0]
    print(url)

    context = {'request': request, 'image_link': url}

    return templates.TemplateResponse('index.html', context=context)




