import anthropic
from youtube_transcript_api import YouTubeTranscriptApi
import os

async def extract_transcript(yt_video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(yt_video_id)
    except Exception as e:
        print(f"Error: {e}")
        return None    
    
    text_transcript = ""
    for i in transcript:
        text_transcript += i['text'] + " "

    return text_transcript

def claude_api_call(message,client):
    try:
        message = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                messages=[
                {"role": "user", "content": f"{message}"}
            ]
        )
        return message.content[0].text
    except Exception as e:
        print(f"Error: {e}")
        return None

async def generate_summary(transcript, client):

    message = f"I want you to summarise this transcipt to a 5min read, do not \
        include any filler messages like 'Here is the summary', the transcript is  - {transcript} \n\n Do not include the prelude"
    
    return claude_api_call(message, client)


async def generate_summary_from_blog(blog_url, client):
    message = f"I want you to summarise this blog to a 5min read, do not \
        include any filler messages like 'Here is the summary', the blog is  - {blog_url} \n\n Do not include the prelude"
    
    return claude_api_call(message, client)

async def generate_script(summary, client):
    message = f"You are a social media manager convert the following summary into a script for \
        a 30s-50s engaging tiktok reel, do not inlcude text like 'Here is a script'. Also do not include any actions the actor takes, \
            only keep speech. \n\n Here is the summary  - {summary} "
    
    return claude_api_call(message, client)

async def generate_image_prompts(script, client):
    message = f"I want to feed this into a text-to-image generator to create a video based on keypoints \
        from the following script, I need 10 phrases to feed into the engine sequenced with timestamps, you should form a narrative of an interesting \
            tiktok video. The video is 30-50s long. Do not include the prelude. The script is - {script} \n\n "

    return claude_api_call(message, client)

async def generate_mcq(summary, client):
    message = f"I want to create 2 multiple choice question based on the following summary, the summary is - {summary} \n\n Format the output is this form 'Question 1:' 'Option 1' 'Option 2' 'Option 3' 'Option 4' 'Answer' \n\n Return this as a json object"

    return claude_api_call(message, client)


async def generate_flash_cards(summary, client):
    message = f"I want to create 4 flash cards based on the following summary. Format the output in this format 'Question1:' 'Answer1:', Return this as a json object, the summary is - {summary} \n\n "

    return claude_api_call(message, client)

if __name__ == "__main__":
    
    yt_video_id = "deQ7ltRsCzw"
    client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"))
    transcript = extract_transcript(yt_video_id)
    if transcript is None:
        print("Error: Could not extract transcript")
        exit(1)
    print("Generating Summary")
    summary = generate_summary(transcript, client)
    # summary = generate_summary_from_blog("https://medium.com/analytics-vidhya/semantic-search-engine-using-nlp-cec19e8cfa7e", client)
    print("Generating Script")
    script = generate_script(summary, client)
    print("Generating Image Prompts")
    image_prompts = generate_image_prompts(script, client)

    print(f"Summary: {summary}")
    print()
    print('='*100)
    print(f"Script: {script}")
    print()
    print('='*100)
    print(f"Image Prompts: {image_prompts}")