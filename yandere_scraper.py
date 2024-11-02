import os
import requests as req
from bs4 import BeautifulSoup as BS

# pages to scrape
yandere_pages = [
    'https://yande.re/post?page=1&tags=tabgraphics', 
    'https://yande.re/post?page=2&tags=tabgraphics',
    'https://yande.re/post?page=3&tags=tabgraphics',
    'https://yande.re/post?page=4&tags=tabgraphics' 
]

def scrape_yandere(urls: list[str]) -> list[str]:

    out = [] 

    for url in urls:

        try:
            res = req.get(url)
            res.raise_for_status()
            
            soup = BS(res.text, 'html.parser')

            # turns out they provide an easy class to get all the links, how nice of them :pray:
            curr_found = [a['href'] for a in soup.find_all('a', href=True, class_= 'directlink largeimg') if a['href'].endswith(('.jpg', '.png'))]  
            out.extend(curr_found)    

        except Exception as e: 
            print(f"Couldn't scrape {url}: {e}... welp")
    
    return out
    
def write_to_file(chosen_file: str, content: list[str]) -> None:
    with os.open(chosen_file, 'a') as file: 
        for entry in content:
            file.print(entry,end = '\n')
