import requests
from bs4 import BeautifulSoup
import json
import re

def extract_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_video_data_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    video_list = []

    # Find the <script> tag with ytInitialData
    yt_data_script = None
    for script in soup.find_all('script'):
        if 'var ytInitialData =' in script.text:
            yt_data_script = script.string
            break
    if not yt_data_script:
        return video_list  # no data found

    # Extract JSON data
    json_text = yt_data_script.split('var ytInitialData =',1)[1].rsplit(';',1)[0].strip()
    data = json.loads(json_text)

    # Navigate to videoRenderer contents
    try:
        contents = data['contents']['twoColumnSearchResultsRenderer']['primaryContents']\
            ['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
    except (KeyError, IndexError):
        return video_list  # structure changed or no videos

    for item in contents:
        if 'videoRenderer' in item:
            video = item['videoRenderer']
            video_id = video.get('videoId')
            title_runs = video.get('title', {}).get('runs', [])
            title = title_runs[0]['text'] if title_runs else 'No title'
            url = f"https://www.youtube.com/watch?v={video_id}"
            thumbnail = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

            # Add video data dict
            video_list.append({
                'title': title,
                'link': url,
                'thumbnail': thumbnail
            })
    return video_list

def get_recommendations(search_query):
    base_url = "https://www.youtube.com/results"
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {'search_query': search_query}

    response = requests.get(base_url, params=params, headers=headers)
    if response.status_code != 200:
        return []

    return get_video_data_from_html(response.text)

