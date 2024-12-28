import util_time_formatter
import json
import requests
import urllib3
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

# i needa get rid of the retarded warnings
urllib3.disable_warnings()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
} # the annoying CBC server was blocking us without the browser header detecting the bot...

articles = {} # dictionary to keep sourceId : (title, url, timestamp, isUpdated = False by default, img)


tracked_categories = [
    "https://www.cbc.ca/lite/news/canada/montreal?sort=latest",
    "https://www.cbc.ca/lite/news/politics?sort=latest",
    "https://www.cbc.ca/lite/news/world?sort=latest"
]

# oh my gah i wish i were a birb D:
async def fetch_news() -> list[tuple[str, str | None]]:
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
                    # let's try to extract a cover picture
                    img_src = await get_img(link) if link else None

                    # if the article was already being tracked
                    if sourceID in articles.keys():
                        if articles[sourceID][2] < timestamp: # if the timestamp has changed, it means the article got updated, then we need to send it again
                            articles[sourceID] = (title, link, timestamp, True, img_src) #isUpdated = True
                            news.append((f"## {title}\n### Updated: {formatted_time}\n {link}\n", f"{img_src}" if img_src else None ))
                    else:
                        articles[sourceID] = (title, link, timestamp, False, img_src)
                        news.append((f"## {title}\n### New: {formatted_time}\n {link}\n", f"{img_src}" if img_src else None))


            else:
                print(f"[!] {util_time_formatter.get_curr_timestamp()} no <script> tag at: ({url})")

        
        else:
            print(f"[!] {util_time_formatter.get_curr_timestamp()} request to CBC Lite ({url}) failed with code = {res.status_code}")

    return news

async def get_img(url:str) -> str | None:
    '''tries to GET-request a cbc.com news page and scrape it to extract the thumbnail then returns a url or None'''
    img_res = requests.get(url, headers=headers, timeout=10, verify=False)
    img_src = None # will return none by default

    if img_res.status_code == 200:
        img_soup = BeautifulSoup(img_res.text, 'html.parser')
        img_script_tag = img_soup.find("script", type="application/ld+json")

        if img_script_tag:
            json_data = json.loads(img_script_tag.string)
            img_src = json_data.get("thumbnailUrl") or None
    
    return img_src


# 




# async def test_em():
    
#     pic = await get_img('https://www.cbc.ca/news/canada/montreal/smog-warning-montreal-boxing-day-1.7419088')
#     print(pic)


# try:
#     asyncio.run(test_em())
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