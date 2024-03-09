import anthropic
from youtube_transcript_api import YouTubeTranscriptApi

def extract_transcript(yt_video_id):
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
                model="claude-instant-1.2",
                max_tokens=4000,
                messages=[
                {"role": "user", "content": f"{message}"}
            ]
        )
        return message.content[0].text
    except Exception as e:
        print(f"Error: {e}")
        return None

def genertate_summary(transcript, client):

    message = f"I want you to summarise this transcipt to a 10min read, do not \
        include any filler messages like 'Here is the summary', the transcript is  - {transcript} \n\n Do not include the prelude"
    
    return claude_api_call(message, client)


def generate_summary_from_blog(blog_url, client):
    message = f"I want you to summarise this blog to a 10min read, do not \
        include any filler messages like 'Here is the summary', the blog is  - {blog_url} \n\n Do not include the prelude"
    
    return claude_api_call(message, client)

def generate_script(summary, client):
    message = f"Convert the summary into a script for \
        a 1-2min video, do not inlcude text like 'Here is a script', summary  - {summary} \n\n Do not include the prelude"
    
    return claude_api_call(message, client)

def generate_image_prompts(script, client):
    message = f"I want to feed this into a visual image generator to create a video based on keypoints \
        from the following script, I need 6 phrases not exceeding 5 words sequenced with timestamps, you should form a narrative. The video is 1 to 2 min long. The script is - {script} \n\n Do not include the prelude"

    return claude_api_call(message, client)


if __name__ == "__main__":
    
    yt_video_id = "deQ7ltRsCzw"
    client = anthropic.Anthropic(
    api_key="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")
    transcript = extract_transcript(yt_video_id)
    if transcript is None:
        print("Error: Could not extract transcript")
        exit(1)
    print("Generating Summary")
    summary = genertate_summary(transcript, client)
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