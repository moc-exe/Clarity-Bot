import util_time_formatter
import json
import requests
from bs4 import BeautifulSoup
import time
import asyncio


# format of the <script> tag on the cbc webpage
'''
{
    "props": {
        "pageProps": {
            "articles": [
                {
                    "components": null,
                    "sourceId": "1.7418732",
                    "title": "Quebec hospital steps into the future with robot tech for knee surgeries",
                    "section": {
                        "path": "News/Canada/Montreal"
                    },
                    "type": "story",
                    "href": "https://www.cbc.ca/news/canada/montreal/robot-technology-quebec-hospital-1.7418732",
                    "updatedAt": "1735068064691"
                },
                {
                    "components": null,
                    "sourceId": "1.7418661",
                    "title": "Workers at Stoneham ski resort in Quebec inch toward 3-day strike",
                    "section": {
                        "path": "News/Canada/Montreal"
                    },
                    "type": "story",
                    "href": "https://www.cbc.ca/news/canada/montreal/stoneham-resort-possible-strike-1.7418661",
                    "updatedAt": "1735062368023"
                },
                {
                    "components": null,
                    "sourceId": "1.7418547",
                    "title": "More immigrants are staying in Quebec, Atlantic Canada struggling with retention, report finds",
                    "section": {
                        "path": "News/Canada/Montreal"
                    },
                    "type": "story",
                    "href": "https://www.cbc.ca/news/canada/montreal/immigration-retention-canada-1.7418547",
                    "updatedAt": "1735057758193"
                }
                // Continue for the rest of the articles...
            ],
            "path": "/news/canada/montreal",
            "selectedSort": "latest",
            "availableSorts": [
                "editors-picks",
                "latest"
            ],
            "categories": [
                {
                    "name": "News",
                    "path": "/news",
                    "slug": "news"
                },
                {
                    "name": "Canada",
                    "path": "/news/canada",
                    "slug": "canada"
                },
                {
                    "name": "Montreal",
                    "path": "/news/canada/montreal",
                    "slug": "montreal"
                }
            ],
            "lineupSlug": "",
            "section": "Montreal",
            "area": "news",
            "referrer": "",
            "headerShowDate": true,
            "skipLink": true
        },
        "__N_SSP": true
    },
    "page": "/[...slug]",
    "query": {
        "sort": "latest",
        "slug": [
            "news",
            "canada",
            "montreal"
        ]
    },
    "buildId": "FYt8rEskyzk2IAC1scgHg",
    "assetPrefix": "/lite",
    "isFallback": false,
    "isExperimentalCompile": false,
    "gssp": true,
    "scriptLoader": []
}
'''

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
} # the annoying CBC server was blocking us without the browser header detecting the bot...

articles = {} # dictionary to keep sourceId : (title, url, timestamp, isUpdated = False by default, img)


tracked_categories = [
    "https://www.cbc.ca/lite/news/canada/montreal?sort=latest",
    "https://www.cbc.ca/lite/news/politics?sort=latest",
    "https://www.cbc.ca/lite/news/world?sort=latest"
]

async def fetch_news() -> list[str]:
    news = []

    for url in tracked_categories:
        
        res = requests.get(url, headers=headers, timeout=10, verify=False)

        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser") # beautiful soup to parse the page
            script_tag = soup.find("script", id="__NEXT_DATA__") # locates and retrieves the <script> tag which is compliant (ideally) with the format above ^^^
            
            if script_tag:

                data = json.loads(script_tag.string)
                curr_articles = data["props"]["pageProps"]["articles"]

                for article in curr_articles:
                    
                    sourceID = article["sourceId"]
                    title = article["title"]
                    link = article["href"]
                    timestamp = int(article["updatedAt"])
                    formatted_time = util_time_formatter.unix_time_to_str(timestamp)
                    img_src = None

                    # let's try to extract a cover picture
                    if link: 
                        img_res = requests.get(link, headers=headers, timeout=10, verify=False)

                        if img_res.status_code == 200:
                            img_soup = BeautifulSoup(img_res.text, 'html.parser')
                            img_src = img_soup.find('img').get('src') or None


                    # if the article was already being tracked
                    if sourceID in articles.keys():
                        if articles[sourceID][2] < timestamp: # if the timestamp has changed, it means the article got updated, then we need to send it again
                            articles[sourceID] = (title, link, timestamp, True, img_src) #isUpdated = True
                            news.append(f"## {title}\n### Updated: {formatted_time}\n {link}\n {img_src if img_src else ''}")
                    else:
                        articles[sourceID] = (title, link, timestamp, False, img_src)
                        news.append(f"## {title}\n### New: {formatted_time}\n {link}\n {img_src if img_src else ''}")


            else:
                print(f"[!] {util_time_formatter.get_curr_timestamp()} no <script> tag at: ({url})")

        
        else:
            print(f"[!] {util_time_formatter.get_curr_timestamp()} request to CBC Lite ({url}) failed with code = {res.status_code}")

    return news

# try:
#     asyncio.run(print_em())
# except Exception as e:
#     print(f"[!] Error running main function: {e}")




# def remove_old_entries():
#     global articles
#     curr_time = int(time.time())  # current Unix timestamp
#     retention_period = 3 * 24 * 60 * 60  # retain articles for 3 days (in seconds)

#     # filter out entries older than the retention period
#     articles = {
#         url: (updated, added_time)
#         for url, (updated, added_time) in articles.items()
#         if curr_time - added_time <= retention_period
#     }
#     print("Old entries removed.")

# @tasks.loop(hours=24)
# async def periodic_cleanup():
#     remove_old_entries()