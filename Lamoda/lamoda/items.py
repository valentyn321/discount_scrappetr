# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LamodaItem(scrapy.Item):
    brand = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    photo = scrapy.Field()
    sizes = scrapy.Field()
    sex = scrapy.Field()
