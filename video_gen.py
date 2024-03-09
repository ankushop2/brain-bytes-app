from moviepy.editor import *
import base64
from io import BytesIO
from PIL import Image
import numpy as np

def transcribe_audio(audio_clip):
    recognizer = sr.Recognizer()
    audio_data = audio_clip.to_soundarray(fps=44100)
    audio_text = recognizer.recognize_google(audio_data)
    return audio_text

def generate_video_from_imgs(img_jsons, audio_file_path):
    audio = AudioFileClip(audio_file_path)
    audio_duration = audio.duration
    image_section_duration = audio_duration / 6
    #Extract base64 strings from JSON
    img_clips = []
    for img_json in img_jsons:
        img = Image.open(BytesIO(base64.b64decode(img_json['artifacts'][0]['base64'])))
        img_clip = ImageClip(np.array(img), duration=5)
        img_duration = min(image_section_duration, audio_duration)
        img_clips.append(img_clip.set_duration(image_section_duration))
        audio_duration -= img_duration

    final_clip = concatenate_videoclips(img_clips, method="compose")
    final_clip = final_clip.set_audio(audio)


    final_clip.write_videofile("output_video.mp4", fps=24)

    return

