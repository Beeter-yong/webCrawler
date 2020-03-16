# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebcrawlerItem(scrapy.Item):
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

