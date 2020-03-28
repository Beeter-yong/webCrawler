# -*- coding: utf-8 -*-
import scrapy
from webCrawler.items import CommunityItem
from webCrawler.utils.logger import Logger
from webCrawler.utils.mysqlUtil import database
import json
# import time
# import random

logger = Logger(name='community')
db = database()


class LianjiaCommunitySpider(scrapy.Spider):
    name = 'lianjia_community'
    allowed_domains = ['bj.lianjia.com']
    start_urls = []
    custom_settings = {
        'ITEM_PIPELINES': {
            'webCrawler.pipelines.DownCommunityInfoPipeline': 101,
        }
    }

    # 开始函数，确定爬取的链接
    def start_requests(self):
        sql = 'SELECT shopingUrl FROM lianjiaShoppingUrl WHERE visited=0'
        shoppingUrls = db.selectSql(sql)
        for shoppingUrl in shoppingUrls:
            try:
                print("正在爬取链接"+shoppingUrl[0])
                yield scrapy.Request(shoppingUrl[0])
                # time.sleep(random.randint(30, 60))
                # break
            except:
                continue

    # 爬取每一个商圈的所有小区
    def parse(self, response):
        xiaoquListItems = response.xpath("//li[@class='clear xiaoquListItem']")
        for xiaoquListItem in xiaoquListItems:
            item = CommunityItem()
            try:
                communityUrl = xiaoquListItem.xpath(".//div[@class='title']/a/@href").get()
                rentUrl_a = xiaoquListItem.xpath(".//div[@class='houseInfo']/a")
                try:
                    if len(rentUrl_a) == 2:
                        item['rentUrl'] = xiaoquListItem.xpath(".//div[@class='houseInfo']/a[2]/@href").get()
                    elif len(rentUrl_a) == 3:
                        item['rentUrl'] = xiaoquListItem.xpath(".//div[@class='houseInfo']/a[3]/@href").get()
                    # 为什么捕获异常，因为有的小区没有出租房源，所以该链接捕获不到
                except:
                    logger.info("该小区没有出租信息" + communityUrl)
                    item['rentUrl'] = None
                item['tag'] = xiaoquListItem.xpath(".//div[@class='tagList']/span/text()").get()
                positionInfo = xiaoquListItem.xpath(".//div[@class='positionInfo']/a")
                item['regional'] = positionInfo[0].xpath("./text()").get()
                item['shopping'] = positionInfo[1].xpath("./text()").get()

                yield scrapy.Request(communityUrl, callback=self.parse_community, meta={'item': item})
                # time.sleep(random.randint(1, 5))
                # break
            except Exception as e:
                logger.error("爬取小区链接时候发生错误---" + response.url)

        pagedata = response.xpath("//div[@class='page-box house-lst-page-box']/@page-data").get()
        pagedata = json.loads(pagedata)
        totalPage = pagedata['totalPage']
        curPage = pagedata['curPage']

        urlfragments = response.url.split("/")
        mainUrl = urlfragments[0] + '//' + urlfragments[2] + '/' + urlfragments[3] + '/' + urlfragments[4] + '/'
        if curPage < totalPage:
            curPage += 1
            nextUrl = mainUrl + 'pg%d/'%curPage
            # print(nextUrl)
            try:
                logger.info("爬取小区的下一页" + nextUrl)
                yield scrapy.Request(nextUrl, callback=self.parse)
                # time.sleep(random.randint(3, 8))
            except:
                logger.error("小区爬取下一页出错" + nextUrl)
        else:
            print("===========================")
            # 当该商圈的所有小区爬取完成后将相应的标志设为1，目的是断点续爬的实现
            sql = "UPDATE lianjiaShoppingUrl SET visited=1 WHERE shopingUrl='%s';"%mainUrl
            db.updateSql(sql)
            logger.info("一条商圈链接爬取完成" + response.url)

    # 进入小区详情页获取小区详情信息
    def parse_community(self, response):
        item = response.meta['item']
        item['communityUrl'] = response.url
        item['communityName'] = response.xpath("//h1[@class='detailTitle']/text()").get()
        try:
            item['communityImg'] = response.xpath("//ol[@id='overviewThumbnail']/li[1]/@data-src").get()
        except:
            logger.error("这个小区没有图片")
            item['communityImg'] = None
        xiaoquInfo = response.xpath("//div[@class='xiaoquInfo']/div")
        item['buildingTime'] = xiaoquInfo[0].xpath("./span[@class='xiaoquInfoContent']/text()").get()
        item['buildingType'] = xiaoquInfo[1].xpath("./span[@class='xiaoquInfoContent']/text()").get()
        item['propertyName'] = xiaoquInfo[3].xpath("./span[@class='xiaoquInfoContent']/text()").get()
        item['propertyFees'] = xiaoquInfo[2].xpath("./span[@class='xiaoquInfoContent']/text()").get()
        item['developer'] = xiaoquInfo[4].xpath("./span[@class='xiaoquInfoContent']/text()").get()
        item['buildingNum'] = xiaoquInfo[5].xpath("./span[@class='xiaoquInfoContent']/text()").get()
        item['houseingNum'] = xiaoquInfo[6].xpath("./span[@class='xiaoquInfoContent']/text()").get()
        item['nearbyStores'] = ''.join(xiaoquInfo[7].xpath("./span[@class='xiaoquInfoContent']//text()").getall())

        yield item
