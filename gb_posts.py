# https://gb.ru/posts

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint
import pandas as pd
import re

month_map = {
    'января': '01', 'февраля': '02', 'марта': '03',
    'апреля': '04', 'мая': '05', 'июня': '06',
    'июля': '07', 'августа': '08', 'сентября': '09',
    'октября': '10', 'ноября': '11', 'декабря': '12'
}

url = "https://gb.ru"

ua = UserAgent()

headers = {"User-Agent": ua.chrome}     # рандомный User-Agent (рандомный chrome)
params = {"page": 1}

session = requests.session()        # открытие сессии (нужно, чтобы прога вела себя как человек)

all_posts = []

while True:

    response = session.get(url+"/posts", headers=headers, params=params)
    soup = BeautifulSoup(response.text, "html.parser")
    post_boxes = soup.find_all("div", {"class": "post-item"})
    if not post_boxes:          # 0, 0.0, '', (), [], {}, None
        break

    for post_box in post_boxes:
        post = {}

        title_info = post_box.find("a", {"class": "post-item__title"})
        post["title"] = title_info.getText()
        post["post_url"] = url + title_info.get("href")

        date_str = post_box.find("div", {"class": "m-t-xs"}).getText()
        for m_ru, m_num in month_map.items():
            date_str = re.sub(m_ru, m_num, date_str)
        post["post_date"] = pd.to_datetime(date_str, format='%d %m %Y')

        post_info = post_box.find("div", {"class": "post-counters-wrapper"}).find_all("span")
        post["views"] = int(post_info[0].getText())
        post["comments"] = int(post_info[1].getText())

        post["description"] = post_box.find("div", {"class": "post-description"}).getText()

        img_tag = post_box.find("img", {"class": "img_preview"})
        post["img_preview"] = img_tag.get("src") if img_tag else None

        all_posts.append(post)

    print(f"Обработана {params['page']} страница")
    params['page'] += 1


# pprint(all_posts)
print(len(all_posts))

df = pd.DataFrame(all_posts)
df.to_csv('gb_posts.csv')
print("Записано в 'gb_posts.csv'!")