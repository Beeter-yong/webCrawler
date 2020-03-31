# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ShoppingItem(scrapy.Item):
    # 商圈链接
    shopingUrl = scrapy.Field()
    shopingName = scrapy.Field()
    shopingRegitional = scrapy.Field()

class CommunityItem(scrapy.Item):
    # 小区信息以及租房链接等信息
    communityUrl = scrapy.Field()   #小区的链接
    communityName = scrapy.Field()  #小区名字
    regional = scrapy.Field()       #所属行政区
    shopping = scrapy.Field()       #所属商圈
    communityImg = scrapy.Field()   #小区图片链接
    rentUrl = scrapy.Field()        #小区的租房链接
    buildingTime = scrapy.Field()   #建筑年代
    buildingType = scrapy.Field()   #建筑类型
    propertyName = scrapy.Field()   #物业公司
    propertyFees = scrapy.Field()   #物业费用
    developer = scrapy.Field()      #开发商
    buildingNum = scrapy.Field()    #楼栋总数
    houseingNum = scrapy.Field()    #房屋总数
    nearbyStores = scrapy.Field()   #附近门店
    tag = scrapy.Field()            #小区标签

class RentItem(scrapy.Item):
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
    timeNew = scrapy.Field()
    rentImg = scrapy.Field()

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
