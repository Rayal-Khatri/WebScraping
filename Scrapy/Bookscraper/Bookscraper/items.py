# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscraperItem(scrapy.Item):
    pass

def serialize_price(value):
    return f'£ {str(value)}'


class BookItem(scrapy.Item):
    url = scrapy.Field()
    title= scrapy.Field()
    product_type = scrapy.Field()
    total_price = scrapy.Field()
    tax =scrapy.Field()
    availability = scrapy.Field()
    no_of_reviews = scrapy.Field()
    stars =scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()