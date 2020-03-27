# -*- coding: utf-8 -*-
import scrapy
from webCrawler.items import ShoppingItem

# 爬取所有商圈的链接，并且存储到数据库
class LianjiaCommunitySpider(scrapy.Spider):
    name = 'lianjia_shopping'
    allowed_domains = ['bj.lianjia.com']
    start_urls = ['https://bj.lianjia.com/xiaoqu/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'webCrawler.pipelines.DownShoppingUrlPipeline': 100,
        }
    }

    def parse(self, response):
        # 爬起所有的行政区链接
        regional_hrefs = response.xpath("//div[@data-role='ershoufang']//a/@href").getall()
        for regional_href in regional_hrefs:
            regional_href = response.urljoin(regional_href)
            yield scrapy.Request(regional_href, callback=self.parse_regional)

    def parse_regional(self, response):
        # 爬取每个行政区的商圈链接
        shopingRegitional = response.xpath("//a[@class='selected']/text()").getall()[2]
        shopping_hrefs = response.xpath("//div[@data-role='ershoufang']/div[2]/a/@href").getall()
        for shopping_href in shopping_hrefs:
            shopingUrl = response.urljoin(shopping_href)
            shopingName = response.xpath("//a[@href='" + shopping_href + "']/text()").get()
            # print(shopingRegitional, shopingUrl, shopingName)
            item = ShoppingItem(shopingUrl=shopingUrl, shopingName=shopingName, shopingRegitional=shopingRegitional)
            yield item

