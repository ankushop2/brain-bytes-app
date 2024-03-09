from flask import Flask
from flask import request
from flask import render_template, jsonify, send_from_directory, send_file
from claude_api import  generate_summary_from_blog, generate_image_prompts, generate_script, generate_mcq
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
        
    tts = gTTS(text=summary, lang='en')
    tts.save("audio.mp3")
    # Generate Script
    script = await generate_script(summary, anthropic_client)
    

    # Generate Image Prompts
    image_prompts = await generate_image_prompts(script, anthropic_client)
    
    prompts = convert_to_array(image_prompts)
    
    # List to hold tasks
    results = []
    
    # Text to image
    for prompt in prompts:
        result = await generate_text_to_image(prompt['phrase'])
        results.append(result)
    
    
    # Video Sitching + Generation
    generate_video_from_imgs(results, "audio.mp3")
    # Upload to UI
    return send_file(
         "output_video.mp4", 
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

    return jsonify({"type":"summary","content":summary})



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
    start = mcq_string.find("```json") + len("```json")
    end = mcq_string.find("```", start)
    mcq_string = mcq_string[start:end]
    questions = json.loads(mcq_string)

    # return jsonify({"type":"mcq","content":mcq})
    return {"type":"quiz-generation", "content":questions}

# comment before deploying
app.run(debug=True)