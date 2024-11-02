import os
import random
import yandere_scraper as ys

yandere_large_pics = ys.scrape_yandere(ys.yandere_pages)

def get_random_local_tabgraphic_path():
    pics = os.listdir("./tabgraphics")
    return "./tabgraphics/" + random.choice(pics)

def get_yandere_url() -> str:
    global yandere_large_pics
    return random.choice(yandere_large_pics)




    
