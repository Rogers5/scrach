# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy

#class ScrachItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass

class DmozItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    tid = scrapy.Field()
    images = scrapy.Field()
    flag = scrapy.Field()
    author = scrapy.Field()