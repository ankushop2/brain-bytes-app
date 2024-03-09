from moviepy.editor import *
import base64
from io import BytesIO

# List of base64 encoded images

base64_images = [
    "YOUR_BASE64_IMAGE_1",
    "YOUR_BASE64_IMAGE_2",
    "YOUR_BASE64_IMAGE_3",
    "YOUR_BASE64_IMAGE_4",
    "YOUR_BASE64_IMAGE_5",
    "YOUR_BASE64_IMAGE_6"
]

# Decode base64 images and store as clips
clips = []
for base64_img in base64_images:
    img_data = base64.b64decode(base64_img)
    img = ImageClip(BytesIO(img_data))
    clips.append(img.set_duration(15))  # Each image for 15 seconds

# Combine clips into a video
final_clip = concatenate_videoclips(clips, method="compose")

# Add audio
audio_base64 = "YOUR_BASE64_AUDIO_FILE"
audio_data = base64.b64decode(audio_base64)
audio = AudioFileClip(BytesIO(audio_data))
final_clip = final_clip.set_audio(audio)

# Export final video
final_clip.write_videofile("output_video.mp4", fps=24)  # Adjust fps as needed
