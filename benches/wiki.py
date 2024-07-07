import bz2
from rich import print

# def count_articles(file_path):
#     article_count = 0
    
    
    
#     with open(file_path, "r", encoding="utf-8") as file:
#         lines = file.readlines()
        
        
#     # choose 100 random entries
#     import random
#     random_lines = random.sample(lines, 100)
    
#     print(random_lines)
        
#     return len(lines)

# if __name__ == "__main__":
#     file_path = "enwiki-20240620-pages-articles-multistream-index.txt"
#     total_articles = count_articles(file_path)
#     print(f"Total number of articles: {total_articles}")


import requests 
from bs4 import BeautifulSoup, Tag
from diskcache import Cache

cache = Cache("cachedir")


# download https://en.wikipedia.org/wiki/User:West.andrew.g/Popular_pages
@cache.memoize()
def download_popular_pages():
    url = "https://en.wikipedia.org/wiki/User:West.andrew.g/Popular_pages"
    response = requests.get(url)
    
    if response.status_code == 200:
        content = response.text
        with open("popular_pages.html", "w", encoding="utf-8") as file:
            file.write(content)
        print("Popular pages downloaded successfully.")
    else:
        print(f"Failed to download. Status code: {response.status_code}")

if __name__ == "__main__":
    download_popular_pages()
    
    pages = BeautifulSoup(open("popular_pages.html"), "html.parser")
    
    # get table
    tbls = pages.find_all("table")
    tbl: Tag = tbls[3]
    snd_cols = [tr.find_all("td")[1].find("a").text for tr in tbl.find_all("tr")[2:]]
    # print(snd_cols)
    
    with open("popular_pages.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(snd_cols))
    
    
    