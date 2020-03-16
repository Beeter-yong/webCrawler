# -*- coding: utf-8 -*-
import scrapy
from webCrawler.items import WebcrawlerItem


class LianjiaCrawlerSpider(scrapy.Spider):
    name = 'lianjia_crawler'
    allowed_domains = ['bj.lianjia.com']
    # start_urls = ['https://bj.lianjia.com/zufang/#contentList']
    start_urls = ['https://bj.lianjia.com/zufang/pg20/#contentList']

    def parse(self, response):
        contentListItems = response.xpath("//div[@class='content__list--item']") #房源列表模块
        for contentListItem in contentListItems:
            houseUrl ='https://bj.lianjia.com' + contentListItem.xpath(".//a[@target='_blank']/@href").get()    #房源链接
            price = contentListItem.xpath(".//span[@class='content__list--item-price']/em/text()").get()    #价格
            addressTag = contentListItem.xpath(".//p[@class='content__list--item--des']//a/text()").getall()
            address = "".join(addressTag)
            regional = addressTag[0]    #区域
            shopping = addressTag[1]    #商圈
            community = addressTag[2]   #小区
            itemTags = contentListItem.xpath(".//p[@class='content__list--item--des']/text()").getall()
            for itemTag in itemTags:
                if '㎡' in itemTag:
                    area = itemTag.strip()  #面积
                elif '室' in itemTag:
                    houseType = itemTag.strip() #房屋结构
                elif '南' in itemTag or '北' in itemTag or '东' in itemTag or '西' in itemTag:
                    towards = itemTag.strip()   #朝向
            floor = contentListItem.xpath(".//span[@class='hide']/text()").getall()[1].replace(' ','').strip()  #层数
            time = contentListItem.xpath(".//span[@class='content__list--item--time oneline']/text()").get()   #最近维护时间

            # print({
            #         'houseUrl': houseUrl, 'price': price, 'area': area, 'houseType': houseType, 'towards': towards,
            #         'address': address, 'regional': regional, 'shopping': shopping,
            #         'community': community, 'floor': floor, 'time': time
            #     })
            item = WebcrawlerItem(houseUrl=houseUrl, price=price, area=area, houseType=houseType, towards=towards,
                                  address=address, regional=regional, shopping=shopping, community=community,
                                  floor=floor, time=time
                                  )
            yield item

        next_url_num = response.xpath("//div[@class='content__pg']/@data-curpage").get()
        if not next_url_num:
            return
        else:
            next_url_num = str(int(next_url_num)+1)
            next_url = 'https://bj.lianjia.com/zufang/pg' + next_url_num + '/#contentList'
            yield scrapy.Request(next_url, callback=self.parse)

