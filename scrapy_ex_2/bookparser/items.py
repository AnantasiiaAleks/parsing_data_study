# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from itemloaders.processors import TakeFirst, MapCompose, Compose

def process_name(value):
    value = value[0].strip()
    return value

def process_price(value):
    value = value[0].replace('₽', ' ').replace('\xa0', '').strip()
    try:
        value[0] = int(value[0])
    except:
        pass
    return value[0]

def process_photo(value):
    print()
    if value.startswith('//'):
        value = 'https:' + value.split()[0]
        return value



class BookparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor=Compose(process_name), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(process_price))
    photos = scrapy.Field(input_process=MapCompose(process_photo))
    _id = scrapy.Field()

