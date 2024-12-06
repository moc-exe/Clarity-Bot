import os
import requests
import util_time_formatter as utf

API_KEY = os.getenv("CLARITY_JSON_API_KEY")
SEARCH_ENGINE_ID = os.getenv("CLARITY_SEARCH_ENGINE_ID")

api_endpoint_base = "https://www.googleapis.com/customsearch/v1"

def web_search(prompt:str, limit:int = None, descriptions:bool = False) -> list[str]:

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
        
        # if snippets of the results are demanded, will be output as well
        if descriptions: 
            results = [
                f" **{index+1} {elem['title']}**: {elem['snippet']} \n {elem['link']}\n\n" for index, elem in enumerate(body.get("items",[]))
            ]
        else:
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


def image_search(prompt:str, color:str=None, limit:int=5, size:str=None, image_type:str=None, custom_link:str=None) -> list[str]:

    # as per docs https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list#response
    allowed_dominant_colors = ("black","blue","brown","gray","green","orange","pink","purple","red","teal","white","yellow")
    allowed_image_sizes = ("huge","icon","large","medium","small","xlarge","xxlarge")
    allowed_image_types = ("clipart","face","lineart","stock","photo","animated")

    query = {
        "key" : API_KEY,
        "cx" : SEARCH_ENGINE_ID,
        "q" : prompt,
        "searchType" : "image"
    }

    if color and str.lower(color) in allowed_dominant_colors:
        query['imgDominantColor'] = str.lower(color)
    if size and str.lower(size) in allowed_image_sizes:
        query['imgSize']=str.lower(size)
    if image_type and str.lower(image_type) in allowed_image_types:
        query['imgType']=str.lower(image_type)
    if custom_link: 
        query['linkSite']=custom_link

    if limit and limit > 0 and limit <= 10: 
        query['num'] = limit

    res = requests.get(api_endpoint_base, params=query)
    
    if res.status_code != 200: 
        print(f'[!] {utf.get_curr_timestamp()} Failed Google Search API request')
        print(f'[!] {utf.get_curr_timestamp()} Status Code = {res.status_code}')
        return ["Request failed. Please try later.\n"]
    
    else:

        body = res.json()
        results = [
                f" {elem['link']}\n" for elem in body.get("items",[])
            ]
        return results