import scrapy
from scrapy.http import HtmlResponse
from scrapy_fst_hw.booksparser.items import BooksparserItem


class LabirintruSpider(scrapy.Spider):
    name = "labirintru"
    allowed_domains = ["labirint.ru"]
    start_urls = ["https://www.labirint.ru/genres/2993/"]

    def parse(self, response:HtmlResponse):

        next_page = response.xpath("//div[@class = 'pagination-next']/a/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//div[@data-title='Все в жанре «Комиксы, Манга, Артбуки»']//a[@class='product-title-link']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)


    def book_parse(self, response:HtmlResponse):
        title = response.xpath("//h1/text()").getall()
        price = response.xpath("//div[contains(@class, 'rubl')]/text()").get()
        desc = response.xpath("//div[contains(@class, '_content_eijg8_12')]//text()").get()
        url = response.url
        yield BooksparserItem(title=title, price=price, desc=desc, url=url)