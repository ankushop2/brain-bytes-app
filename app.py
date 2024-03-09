from flask import Flask
from flask import request
import os
import base64
import requests

stability_url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"

app = Flask(__name__)

def generate_text_to_image(text_prompt):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer "+os.environ.get('STABILITY_API_KEY'),
    }
    
    body = {
        "steps": 40,
        "width": 512,
        "height": 512,
        "seed": 0,
        "cfg_scale": 5,
        "samples": 1,
        "text_prompts": [
            {
                "text": text_prompt,
                "weight": 1
            },
        ],
    }
    
    response = requests.request("POST", stability_url, json=body, headers=headers)
    return response.json


@app.route('/video', methods=["POST"])
def generate_video():
    # Parse JSON from UI
    data = request.get_json()
    url = data.get('URL')
    
    # Determine the Type of URL
    
    
    # Generate Transcript / Text 
    
    # Summarize using LLM
    
    # Text to Image 

    print(generate_text_to_image('A lighthouse on a cliff'))
    
    # Text to speech
    
    # Generate Captions
    
    # Video Sitching + Generation
    
    # Upload to VIMEO
    return 'Hello, World!'


@app.route("/audio", methods=["POST"])
def generate_audio():
    # Parse JSON from UI
    data = request.get_json()
    url = data.get('URL')
    
    # Determine the Type of URL 
    
    # Generate Transcript / Text 
    
    # Summarize using LLM
    
    # Text to speech
    
    return 'Hello World!'

@app.route("/summary", methods=["POST"])
def generate_summary():
    
    # Parse JSON from UI
    data = request.get_json()
    url = data.get('URL')
    
    # Determine the Type of URL 
    
    # Generate Transcript / Text 
    
    # Summarize using LLM
    
    return 'Hello World!'


@app.route('/quiz-generation', methods=["POST"])
def quiz_generation():
    # Parse JSON from UI
    data = request.get_json()
    url = data.get('URL')
    
    # Determine the Type of URL 
    
    # Generate Transcript / Text 
    
    # Summarize using LLM and generate questions
    return 'Hello World!'


# comment before deploying
