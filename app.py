from flask import Flask
from flask import request
from flask import render_template, jsonify, send_from_directory, send_file
from claude_api import  generate_summary_from_blog, generate_image_prompts, generate_script, generate_mcq, generate_flash_cards
from captions import create_captions
from claude_api import extract_transcript
from utils import determine_url_type_and_extract_id
from gtts import gTTS
from video_gen import generate_video_from_imgs
import os
import base64
import requests
import anthropic
import claude_api
import asyncio
import json
import requests

stability_url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"

app = Flask(__name__, template_folder="templates")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route("/")
def hello_world():
    return render_template('index.html')

def convert_to_array(text):
    # Splitting the text into lines
    lines = text.split("\n")

    # Removing the first line as it's not part of the timestamped phrases
    lines = lines[1:]

    # Creating an array of dictionaries with timestamp and phrase fields
    prompts = []
    for line in lines:
        if " - " in line:
            timestamp, phrase = line.split(" - ", 1)
            prompts.append({"timestamp": timestamp, "phrase": phrase})
        else:
            print(f"Ignoring line: {line}")
    return prompts

async def generate_text_to_image(text_prompt):
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
    return response.json()


@app.route('/video', methods=["POST"])
async def generate_video():
    # Parse JSON from UI
    data = request.get_json()
    url = data.get('URL')
    print(url)
    
    # Determine the Type of URL
    
    url_type, id_or_url = determine_url_type_and_extract_id(url)
    if url_type == "YouTube":
        print("YouTube Video ID:", id_or_url)
    elif url_type == "Medium":
        print("Medium URL:", id_or_url)
    # Generate Transcript / Text 
    if url_type=='YouTube':
        text = await  extract_transcript(id_or_url)

    # Summarize using LLM
    anthropic_client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    if url_type=='YouTube':
        summary = await claude_api.generate_summary(text,anthropic_client)
    else:
        summary = await generate_summary_from_blog(id_or_url, anthropic_client)
    
    #Generate audio 
        
    
    # Generate Script
    script = await generate_script(summary, anthropic_client)
    print(script)
    
    tts = gTTS(text=summary, lang='en')
    tts.save("audio.mp3")

    # Generate Image Prompts
    image_prompts = await generate_image_prompts(script, anthropic_client)

    print(image_prompts)
    
    prompts = convert_to_array(image_prompts)
    
    # List to hold tasks
    results = []
    
    # Text to image
    for prompt in prompts:
        result = await generate_text_to_image(prompt['phrase'])
        results.append(result)
    
    
    # Video Sitching + Generation
    generate_video_from_imgs(results, "audio.mp3")

    create_captions("output_video.mp4")

    # Upload to UI
    return send_file(
         "output-output_video.mp4", 
         mimetype="video/mp4", 
         as_attachment=True)


@app.route("/audio", methods=["POST"])
async def generate_audio():
    # Parse JSON from UI
    data = request.get_json()
    url = data.get('URL')

    #Determine the Type of URL

    type, id_or_url = determine_url_type_and_extract_id(url)
    if type == "YouTube":
        print("YouTube Video ID:", id_or_url)
    elif type == "Medium":
        print("Medium URL:", id_or_url)

#Generate Transcript / Text
    if type=='YouTube':
        text = await  extract_transcript(id_or_url)

    # Summarize using LLM
    anthropic_client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"))

    if type=='YouTube':
        summary = await claude_api.generate_summary(text,anthropic_client)
    else:
        summary = await generate_summary_from_blog(id_or_url, anthropic_client)

#Text to speech
    speechAudio = gTTS(text=summary, lang='en', slow=False)
    speechAudio.save("tts.wav")
    return send_file(
         "tts.wav", 
         mimetype="audio/wav", 
         as_attachment=True)

@app.route("/summary", methods=["POST"])
async def generate_summary():
    # Parse JSON from UI
    data = request.get_json()
    url = data.get('URL')

    #Determine the Type of URL

    type, id_or_url = determine_url_type_and_extract_id(url)
    if type == "YouTube":
        print("YouTube Video ID:", id_or_url)
    elif type == "Medium":
        print("Medium URL:", id_or_url)

#Generate Transcript / Text
    if type=='YouTube':
        text = await  extract_transcript(id_or_url)

    # Summarize using LLM
    anthropic_client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"))

    if type=='YouTube':
        summary = await claude_api.generate_summary(text,anthropic_client)
    else:
        summary = await generate_summary_from_blog(id_or_url, anthropic_client)


    translate_api_url = "https://655.mtis.workers.dev/translate"
    translate_params_fr = {
    'text': summary,  # The text you want to translate
    'source_lang': 'en',    # Optional: The source language (defaults to English)
    'target_lang': 'fr'     # Optional: The target language (defaults to French)
    }

    translate_params_it = {
    'text': summary,  # The text you want to translate
    'source_lang': 'en',    # Optional: The source language (defaults to English)
    'target_lang': 'it'     # Optional: The target language (defaults to French)
    }

    response_fr = requests.get(translate_api_url, params=translate_params_fr) 
    if response_fr.status_code == 200:
        data = response_fr.json()
        summary_fr = data['response']['translated_text']

    response_it = requests.get(translate_api_url, params=translate_params_it) 
    if response_it.status_code == 200:
        data = response_it.json()
        summary_it = data['response']['translated_text']

    return jsonify({"type":"summary","content":{"summary_en":summary,"summary_fr":summary_fr,"summary_it":summary_it}})



@app.route('/quiz-generation', methods=["POST"])
async def quiz_generation():
    # Parse JSON from UI
    data = request.get_json()
    url = data.get('URL')
    
    # Determine the Type of URL 

    type, id_or_url = determine_url_type_and_extract_id(url)
    if type == "YouTube":
        print("YouTube Video ID:", id_or_url)
    elif type == "Medium":
        print("Medium URL:", id_or_url)

    #Generate Transcript / Text
    if type=='YouTube':
        text = await  extract_transcript(id_or_url)
    
    # Generate Transcript / Text 
    anthropic_client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"))

    if type=='YouTube':
        summary = await claude_api.generate_summary(text,anthropic_client)
    else:
        summary = await generate_summary_from_blog(id_or_url, anthropic_client)


    # Summarize using LLM and generate questions
        
    mcq_string = await generate_mcq(summary, anthropic_client)
    # print(mcq_string)
    # start = mcq_string.find("```json") + len("```json")
    # end = mcq_string.find("```", start)
    # mcq_string = mcq_string[start:end]
    # questions = json.loads(mcq_string)
    print(mcq_string)
    return {"type":"quiz-generation","content":mcq_string}
    # return {"type":"quiz-generation", "content":mcq_string}

@app.route('/flash-cards', methods=["POST"])
async def flash_cards():
    # Parse JSON from UI
    data = request.get_json()
    url = data.get('URL')
    
    # Determine the Type of URL 

    type, id_or_url = determine_url_type_and_extract_id(url)
    if type == "YouTube":
        print("YouTube Video ID:", id_or_url)
    elif type == "Medium":
        print("Medium URL:", id_or_url)

    #Generate Transcript / Text
    if type=='YouTube':
        text = await  extract_transcript(id_or_url)
    
    # Generate Transcript / Text 
    anthropic_client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"))

    if type=='YouTube':
        summary = await claude_api.generate_summary(text,anthropic_client)
    else:
        summary = await generate_summary_from_blog(id_or_url, anthropic_client)


    # Summarize using LLM and generate questions
        
    mcq_string = await generate_flash_cards(summary, anthropic_client)
    # print(mcq_string)
    # start = mcq_string.find("```json") + len("```json")
    # end = mcq_string.find("```", start)
    # mcq_string = mcq_string[start:end]
    # questions = json.loads(mcq_string)
    print(mcq_string)
    return {"type":"flash-cards","content":mcq_string}

# comment before deploying
app.run(debug=True, port=5001)