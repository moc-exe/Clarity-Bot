import os
from googleapiclient.discovery import build

YT_API_KEY = os.getenv("CLARITY_YOUTUBE_PUBLIC_API_KEY")

def public_yt_query(query:str, limit:int = 1) -> str:

    client = build("youtube", 'v3', developerKey=YT_API_KEY)

    res = client.search().list(

        part = 'snippet', # idk why but the docs say so 
        q = query,
        maxResults = limit,
        type = 'video'

    ).execute()

    id = res['items'][0]['id']['videoId']
    return f"https://www.youtube.com/watch?v={id}"

