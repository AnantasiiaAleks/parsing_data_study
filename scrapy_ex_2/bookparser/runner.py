from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from spiders.book24 import Book24Spider

if __name__ == '__main__':
    configure_logging()
    install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
    process = CrawlerProcess(get_project_settings())
    # query = input('Введите жанр: ')
    process.crawl(Book24Spider, query='детектив')
    process.start()