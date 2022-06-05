import requests

from bs4 import BeautifulSoup

import pandas as pd


URL = "https://www.imdb.com/chart/top/"

r = requests.get(URL)


dict_data = {"rank": [], "movie": [], "rating": []}

soup = BeautifulSoup(r.text, "lxml")
# print(soup.find("tbody"))
count = 0
for mv_name, rating in zip(
    soup.find_all("td", class_="titleColumn"),
    soup.find_all("td", class_="ratingColumn imdbRating"),
):

    print(i.text, j.text)

    count += 1
    dict_data["rank"].append(count)
    dict_data["movie"].append(mv_name)
    dict_data["rating"].append(rating)
    if count == 5:
        break

df = pd.DataFrame(dict_data)

df.to_csv("file1.csv", index=False)
