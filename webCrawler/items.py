# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class WebcrawlerItem(scrapy.Item):
    # 房源信息
    houseUrl = scrapy.Field()
    price = scrapy.Field()
    area = scrapy.Field()
    houseType = scrapy.Field()
    towards = scrapy.Field()
    address = scrapy.Field()
    regional = scrapy.Field()
    shopping = scrapy.Field()
    community = scrapy.Field()
    floor = scrapy.Field()
    time = scrapy.Field()

class ShoppingItem(scrapy.Item):
    # 商圈链接
    shopingUrl = scrapy.Field()
    shopingName = scrapy.Field()
    shopingRegitional = scrapy.Field()
