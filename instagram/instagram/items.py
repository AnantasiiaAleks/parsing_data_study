# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramItem(scrapy.Item):
    # define the fields for your item here like:
    text = scrapy.Field()
    photo = scrapy.Field()
    post_data = scrapy.Field()
    username = scrapy.Field()
    user_id = scrapy.Field()
    pass
