from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/video', methods=["POST"])
def generate_video():
    # Parse JSON from UI
    data = request.get_json()
    url = data.get('URL')
    print(url)
    
    # Determine the Type of URL
    
    
    # Generate Transcript / Text 
    
    # Summarize using LLM
    
    # Text to Image 
    
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
