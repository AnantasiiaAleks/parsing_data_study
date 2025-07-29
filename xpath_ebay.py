from lxml import html
import requests
from fake_useragent import UserAgent
from pprint import pprint

ua = UserAgent()

headers = {"User-Agent": ua.firefox}

url = 'https://www.ebay.com'
response = requests.get(url + '/e/toys/pop-mart', headers=headers)
dom = html.fromstring(response.text)

items_list = []
items = dom.xpath("//ul[contains(@class, 'brwrvr__item-results')]/li")

for item in items:
    item_info = {}

    name = item.xpath(".//h3[contains(@class, 'bsig__title__text')]/text()")
    link = item.xpath(".//h3[contains(@class, 'bsig__title__text')]/../@href")
    price = item.xpath(".//span[contains(@class, 'bsig__price')]//text()")
    add_info = item.xpath(".//span[contains(@class, 'negative')]/text()")     # не всюду есть, поэтому другой подход

    item_info['name'] = name
    item_info['link'] = link
    item_info['price'] = price
    item_info['add_info'] = add_info

    items_list.append(item_info)

# print()
pprint(items_list)