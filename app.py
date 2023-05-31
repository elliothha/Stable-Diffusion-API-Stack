import json
import requests

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# ---------------------------------------------- API Endpoint Calls ------------------------------------------------------

# returnPrediction calls the API 'Prediction' endpoint
# INPUTS: 
#       pos = "positive" input text of what the user wants to see, entered in corresponding textarea in the HTML form
#       neg = "negative" input text of what the user doesn't want to see
# OUTPUTS:
#       data = JSON formatted output of the API 'Prediction' endpoint call

def returnPrediction(pos, neg):

    # Local path to OpenAPI Spec downloaded from Morgenrot API
    with open('openapi.json') as file:
        json_data = json.load(file)

    # Specific endpoint in the API for generating images
    url = 'https://api.ai8pool.com/v1/predictions'

    # Lets our API call know that we're intaking JSON data and have authorization
    # Token obtained from Richard, or the Create New App call with an authorized login
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer <YOUR_TOKEN_HERE>"
    }

    # The actual data that we feed to the endpoint call
    # Pretty much the only things that vary are the text inputs via the variable input
    # Unsure if guidanceScale and scheduler are actually needed
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

    # requests.post(url, headers, json) is the raw output from calling the API endpoint
    # INPUTS:
    #       url = specific endpoint url
    #       headers = input type/authorization token
    #       json = the payload data sent as JSON data to use
    # OUTPUTS:
    #       response = raw output data, unformatted

    response = requests.post(url=url, headers=headers, json=payload)

    # 200 = Success, 401 = Unauthorized
    # print(f"Response Code: {response.status_code}")
    
    # format the raw data into a JSON format and return
    data = response.json()

    return data


# -------------------------------------------------- FastAPI Routing -------------------------------------------------------


app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.post('/process_inputs')
async def process_inputs(request: Request):
    form_data = await request.form()
    pos = form_data['positive_input']
    neg = form_data['negative_input']

    if not pos:
        pos = " "
    if not neg:
        neg = " "

    print(pos)
    print(neg)
    
    data = returnPrediction(pos=pos, neg=neg)

    print(data)

    image_url = data['output']['urls'][0]

    print(image_url)

    return templates.TemplateResponse('index.html', {'request': request, 'image_url': image_url})

