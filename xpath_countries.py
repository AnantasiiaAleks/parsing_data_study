from lxml import html
import requests
from fake_useragent import UserAgent
from pprint import pprint
import csv

ua = UserAgent()

headers = {"User-Agent": ua.firefox}

url = 'https://www.scrapethissite.com'
response = requests.get(url + '/pages/simple/', headers=headers)
dom = html.fromstring(response.text)


items_list = []
items = dom.xpath("//div[@class='col-md-4 country']")       # блоки

for item in items:
    item_info = {}

    country_name = item.xpath(".//h3[@class='country-name']/text()")
    capital = item.xpath(".//span[@class='country-capital']/text()")
    population = item.xpath(".//span[@class='country-population']/text()")
    area = item.xpath(".//span[@class='country-area']/text()")



    item_info['country_name'] = ' '.join(''.join(country_name).split())     # убрали лишние пробелы и \n
    item_info['capital'] = capital[0]   # вытащить из списка
    try:
        item_info['population'] = int(population[0])   # вытащить из списка и перевести в int
    except:
        item_info['population'] = population
        print("Exception with population, object = ", item_info['population'])
    try:
        item_info['area'] = float(area[0])      # вытащить из списка и перевести в float
    except:
        item_info['area'] = area
        print("Exception with area, object = ", item_info['area'])


    items_list.append(item_info)        # записать все в список словарей

with open('countries.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = items_list[0].keys()  # чтобы не вручную: ['country_name', 'capital', 'area', 'population']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # записываем заголовки
    writer.writerows(items_list)  # записываем все строки