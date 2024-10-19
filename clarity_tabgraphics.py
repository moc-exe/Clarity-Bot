import os
import random
def get_random_tabgraphic_path():
    pics = os.listdir("./tabgraphics")
    return "./tabgraphics/" + random.choice(pics)
