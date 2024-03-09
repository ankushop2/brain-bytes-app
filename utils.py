import re

def determine_url_type_and_extract_id(url):
    # YouTube URL regex
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)'
        '([^&?/\s]{11})'
    )
    
    # Medium URL regex
    medium_regex = r'https:\/\/*medium\.com\/*'
    medium_match = re.match(medium_regex, url)
    # Check if it's a YouTube URL
    youtube_match = re.match(youtube_regex, url)
    if youtube_match:
        return "YouTube", youtube_match.group(4)
    elif medium_match:
        return "Medium", url

    # # Check if it's a Medium URL
    # elif medium_match:
    #     return "Medium", url