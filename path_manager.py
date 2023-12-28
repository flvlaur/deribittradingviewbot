import os

# relative path from root dir (/home/Users/laur/Desktop/deribit-tv-bot)
def path(dir):
    root_dir = os.path.dirname(os.path.abspath("__file__"))
    return root_dir + "/" + dir