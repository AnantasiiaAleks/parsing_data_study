'''
Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/
и извлечь информацию о всех книгах на сайте во всех категориях:
название, цену, количество товара в наличии (In stock (19 available))
в формате integer, описание.
Затем сохранить эту информацию в JSON-файле.
'''

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
import re
from urllib.parse import urljoin
import json

ua = UserAgent()
headers = {"User-Agent": ua.chrome}

base_url = "https://books.toscrape.com/"

all_books = []
page = 1

while True:

    url = f"{base_url}catalogue/page-{page}.html"
    response = requests.get(url, headers=headers)

    if not response.ok:
        print("Больше страниц нет.")
        break

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", {"class": "product_pod"})

    if not books:
        print("Книги не найдены.")
        break

    for book in books:
        book_info = {}
        # Получаем относительную ссылку
        relative_link = "catalogue/" + book.find("h3").find("a")["href"]
        book_url = urljoin(base_url, relative_link)  # Абсолютная ссылка на книгу

        # Парсим страницу книги
        book_response = requests.get(book_url, headers=headers)
        book_soup = BeautifulSoup(book_response.text, "html.parser")

        product_page = book_soup.find("article", {"class": "product_page"})

        if not product_page:
            continue

        book_info["title"] = product_page.find("h1").get_text(strip=True)

        price_str = product_page.find("p", {"class": "price_color"}).get_text(strip=True)
        book_info["price"] = float(re.search(r'\d+\.?\d*', price_str).group())

        availability = product_page.find("p", {"class": "instock availability"}).get_text(strip=True)
        quantity_match = re.search(r'\((\d+)\s+available', availability)
        book_info["quantity"] = int(quantity_match.group(1)) if quantity_match else None

        description_tag = product_page.find("div", {"id": "product_description"})
        raw_description = description_tag.find_next("p").get_text(strip=True) if description_tag else ""
        book_info["description"] = raw_description.encode('latin1').decode('utf-8')

        all_books.append(book_info)
    print(f"Обработана {page} страница")
    page += 1

print(f"Всего обработано книг: {len(all_books)}")

# Сохраняем в CSV
df_csv = pd.DataFrame(all_books)
df_csv.to_csv('books_toscrape.csv', index=False, encoding='utf-8-sig')
print("Записано в 'books_toscrape.csv'!")

# Сохраняем в json
with open('books_toscrape.json', 'w', encoding='utf-8') as f:
    json.dump(all_books, f, ensure_ascii=False, indent=4)
print("Записано в 'books_toscrape.json'!")

