# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field

class CompItem(scrapy.Item):

    name = Field()
    date = Field()
    price = Field()
    proc = Field()
    freq = Field()
    mem = Field()
    hdd = Field()
    link = Field()

