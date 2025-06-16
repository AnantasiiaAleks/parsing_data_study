# https://api.giphy.com/v1/gifs/search  ?
# api_key=api_key  &
# q=programming  &
# limit=5  &
# offset=0  &
# rating=pg-13  &
# lang=ru&bundle=messaging_non_clips

import os
import requests
import json
from dotenv import load_dotenv
from pprint import pprint

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
url = "https://api.giphy.com/v1/gifs/search"

params = {"api_key":"F0MmUVeftlpOd3PQKEt4bYayqfYofz1n",
          "q":"programming",
          "limit":5,
          "offset":0,
          "rating":"pg-13",
          "lang":"ru",
          "bundle":"messaging_non_clips"}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
           "Accept": "*/*"}

response = requests.get(url, params=params, headers=headers)

j_data = response.json()

with open('gifs.json', 'w') as f:
    json.dump(j_data, f)

for gif in j_data.get('data'):
    print(gif.get('images').get('original').get('url'))

pprint(j_data)
# print()





# print()
#
# response.headers
# response.status_code
# response.ok
# response.text
# response.content        # как текст, только бинарный
#
# if response.status_code == 200:
#     print("Do something")
# else:
#     pass
#
# if response.ok:
#     print("Do something")
# else:
#     pass
#
