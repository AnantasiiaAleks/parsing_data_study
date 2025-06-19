import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import json
from fake_useragent import UserAgent

ua = UserAgent()
HEADERS = {"User-Agent": ua.chrome}

BASE_URL = "https://books.toscrape.com/"

all_books = []
seen_books = set()  # чтобы избежать дубликатов


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.read()  # Возвращаем байты


async def parse_book_page(session, book_url):
    try:
        html_bytes = await fetch(session, book_url)
        soup = BeautifulSoup(html_bytes, "html.parser")

        product_page = soup.find("article", {"class": "product_page"})

        if not product_page:
            return None

        title = product_page.find("h1").get_text(strip=True)

        price_str = product_page.find("p", {"class": "price_color"}).get_text(strip=True)
        price = float(re.search(r'\d+\.?\d*', price_str).group())

        availability = product_page.find("p", {"class": "instock availability"}).get_text(strip=True)
        quantity_match = re.search(r'\((\d+)\s+available', availability)
        quantity = int(quantity_match.group(1)) if quantity_match else None

        description_tag = product_page.find("div", {"id": "product_description"})
        raw_description = description_tag.find_next("p").get_text(strip=True) if description_tag else ""

        return {
            "title": title,
            "price": price,
            "quantity": quantity,
            "description": raw_description
        }
    except Exception as e:
        print(f"Ошибка при обработке {book_url}: {e}")
        return None


async def parse_page(session, page_num):
    url = f"{BASE_URL}catalogue/page-{page_num}.html"
    print(f"Обрабатывается страница {page_num}...")

    html = await fetch(session, url)
    soup = BeautifulSoup(html, "html.parser")
    books = soup.find_all("article", {"class": "product_pod"})

    if not books:
        print(f"Страница {page_num} не содержит книг.")
        return False

    tasks = []
    for book in books:
        relative_link = "catalogue/" + book.find("h3").find("a")["href"]
        book_url = urljoin(BASE_URL, relative_link)

        if book_url in seen_books:
            continue
        seen_books.add(book_url)

        tasks.append(parse_book_page(session, book_url))

    results = await asyncio.gather(*tasks)
    for result in results:
        if result:
            all_books.append(result)

    return True


async def main():
    page = 1
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        while True:
            success = await parse_page(session, page)
            if not success:
                break
            page += 1

    print(f"Всего обработано: {len(all_books)} книг.")


    # Сохранение в JSON
    with open("books_toscrape.json", "w", encoding="utf-8") as f:
        json.dump(all_books, f, ensure_ascii=False, indent=4)
    print("Записано в 'books_toscrape.json'!")


if __name__ == "__main__":
    asyncio.run(main())