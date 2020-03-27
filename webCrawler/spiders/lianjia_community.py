# -*- coding: utf-8 -*-
import scrapy
from webCrawler.items import CommunityItem
from webCrawler.utils.logger import Logger
from webCrawler.utils.mysqlUtil import database
import json

logger = Logger(name='community')
db = database()


class LianjiaCommunitySpider(scrapy.Spider):
    name = 'lianjia_community'
    allowed_domains = ['bj.lianjia.com']
    start_urls = []

    def start_requests(self):
        sql = 'SELECT shopingUrl FROM lianjiaShoppingUrl WHERE visited=0'
        shoppingUrls = db.selectSql(sql)
        for shoppingUrl in shoppingUrls:
            try:
                yield scrapy.Request(shoppingUrl[0])
                break
            except:
                continue

    def parse(self, response):
        xiaoquListItems = response.xpath("//li[@class='clear xiaoquListItem']")
        for xiaoquListItem in xiaoquListItems:
            item = CommunityItem()
            try:
                communityUrl = xiaoquListItem.xpath(".//div[@class='title']/a/@href").get()
                try:
                    # 为什么捕获异常，因为有的小区没有出租房源，所以该链接捕获不到
                    item['rentUrl'] = xiaoquListItem.xpath(".//div[@class='houseInfo']/a[2]/@href").get()
                except:
                    logger.info("该小区没有出租信息" + communityUrl)
                    item['rentUrl'] = None
                item['tag'] = xiaoquListItem.xpath(".//div[@class='tagList']/span/text()").get()
                positionInfo = xiaoquListItem.xpath(".//div[@class='positionInfo']/a")
                item['regional'] = positionInfo[0].xpath("./text()").get()
                item['shopping'] = positionInfo[1].xpath("./text()").get()

                yield scrapy.Request(communityUrl, callback=self.parse_community, meta={'item': item})
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
            print(nextUrl)
            try:
                logger.info("爬取小区的下一页" + nextUrl)
                yield scrapy.Request(nextUrl, callback=self.parse)
            except:
                logger.error("小区爬取下一页出错" + nextUrl)
        else:
            print("===========================")
            # 当该商圈的所有小区爬取完成后将相应的标志设为1，目的是断点续爬的实现
            sql = "UPDATE lianjiaShoppingUrl SET visited=1 WHERE shopingUrl='%s';"%mainUrl
            db.updateSql(sql)
            db.close()
            logger.info("一条商圈链接爬取完成" + response.url)

    def parse_community(self, response):
        item = response.meta['item']
        item['communityUrl'] = response.url
        item['communityName'] = response.xpath("//h1[@class='detailTitle']/text()").get()
        try:
            item['communityImg'] = response.xpath("//ol[@id='overviewThumbnail']/li[1]/@data-src").get()
        except:
            logger.error("这个社区没有图片")
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

        print(item)
