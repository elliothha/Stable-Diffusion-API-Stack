import json
import requests

from flask import Flask, render_template, request

def returnPrediction(pos, neg):
    with open('openapi.json') as file:
        json_data = json.load(file)

    url = 'https://api.ai8pool.com/v1/predictions'

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer <YOUR_TOKEN_HERE>"
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
    # print(data['output']['urls'])

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    positiveInput = request.form['positive_input']
    negativeInput = request.form['negative_input']
    if not positiveInput:
        positiveInput = " "
    if not negativeInput:
        negativeInput = " "

    data = returnPrediction(pos=positiveInput, neg=negativeInput)
    url = data['output']['urls'][0]

    return render_template('index.html', image_link=url)




