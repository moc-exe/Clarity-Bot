import os
import requests
import util_time_formatter as utf

API_KEY = os.getenv("CLARITY_JSON_API_KEY")
SEARCH_ENGINE_ID = os.getenv("CLARITY_SEARCH_ENGINE_ID")

api_endpoint_base = "https://www.googleapis.com/customsearch/v1"

def web_search(prompt:str, limit:int = None) -> list[str]:

    query = {
        "key" : API_KEY,
        "cx" : SEARCH_ENGINE_ID,
        "q" : prompt
    }

    if limit and limit > 0 and limit <= 10: 
        query['num'] = limit

    res = requests.get(api_endpoint_base, params=query)
    
    if res.status_code != 200: 
        print(f'[!] {utf.get_curr_timestamp()} Failed Google Search API request')
        print(f'[!] {utf.get_curr_timestamp()} Status Code = {res.status_code}')
        return ["Request failed. Please try later\n"]
    
    else:

        body = res.json()
        results = [
            f" **{index+1} {elem['title']}** : {elem['link']}\n\n" for index, elem in enumerate(body.get("items",[]))
        ]
        return results


def format_web_search(to_format:list[str]) -> list[str]:

    out = []
    curr_str = ""
    counter = 0;
    for elem in to_format: 
        
        counter += len(elem)
        
        if counter <= 1600:
            curr_str += elem
        else:
            out.append(curr_str)
            curr_str = elem
            counter = len(elem)
    
    out.append(curr_str)
    return out


def image_search(prompt:str, color:str = None, limit:int = 10) -> str:
    pass
