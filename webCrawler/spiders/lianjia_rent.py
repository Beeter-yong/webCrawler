# -*- coding: utf-8 -*-
import scrapy
import datetime
from webCrawler.utils.mysqlUtil import database
from webCrawler.utils.logger import Logger
from webCrawler.items import RentItem
db = database()
logger = Logger(name='rent')


class LianjiaRentSpider(scrapy.Spider):
    name = 'lianjia_rent'
    allowed_domains = ['bj.lianjia.com']
    start_urls = ['http://bj.lianjia.com/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'webCrawler.pipelines.DownRentInfoPipeline': 99,
        }
    }

    def start_requests(self):
        #开始函数，确定爬取的链接
        # sql = "SELECT rentUrl FROM lianjiaCommunityInfo WHERE rentUrl!='None'"
        sql = "SELECT rentUrl FROM lianjiaCommunityInfo WHERE rentUrl!='None' AND visited=0"
        # sql = "SELECT rentUrl FROM lianjiaCommunityInfo WHERE shopping='广安门' AND rentUrl!='None'"
        renUrls = db.selectSql(sql)
        for rentUrl in renUrls:
            try:
                logger.info('正在爬取' + rentUrl[0])
                yield scrapy.Request(rentUrl[0], callback=self.parse)
            except Exception as e:
                logger.error("爬取小区租房链接出错")
                logger.error(e)
                continue


    def parse(self, response):
        # 爬取房源信息
        rentNum = response.xpath("//span[@class='q']/text()").get()
        rentNum = rentNum.replace('小区在租：', '')
        rentNum = rentNum.replace('套', '')
        if '0' != rentNum:
            contentListItems = response.xpath("//div[@class='content__list'][1]//div[@class='content__list--item']") #房源列表模块
            for contentListItem in contentListItems:
                try:
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
                        elif '卫' in itemTag:
                            houseType = itemTag.strip() #房屋结构
                        elif '南' in itemTag or '北' in itemTag or '东' in itemTag or '西' in itemTag:
                            towards = itemTag.strip()   #朝向
                    floor = contentListItem.xpath(".//span[@class='hide']/text()").getall()[1].replace(' ','').strip()  #层数
                    time = contentListItem.xpath(".//span[@class='content__list--item--time oneline']/text()").get()   #最近维护时间
                    timeNew = datetime.datetime.now().strftime("%Y-%m-%d")
                    rentImg = contentListItem.xpath("./a/img/@data-src").get()
                    if '250x182' in rentImg:
                        rentImg = rentImg.replace('250x182', '780x439')
                    else:
                        rentImg = None

                    # print({
                    #         'houseUrl': houseUrl, 'price': price, 'area': area, 'houseType': houseType, 'towards': towards,
                    #         'address': address, 'regional': regional, 'shopping': shopping,
                    #         'community': community, 'floor': floor, 'time': time, 'timeNew': timeNew
                    #     })
                    item = RentItem(houseUrl=houseUrl, price=price, area=area, houseType=houseType, towards=towards,
                                          address=address, regional=regional, shopping=shopping, community=community,
                                          floor=floor, time=time, timeNew=timeNew, rentImg=rentImg
                                          )
                    yield item
                    # break
                except Exception as e:
                    logger.error("出现了小区租房链接却租房数为空")
                    continue

            pagedata = response.xpath("//div[@class='content__pg']")
            totalPage = pagedata.xpath("./@data-totalpage").get()
            curPage = pagedata.xpath("./@data-curpage").get()


            urlNow = response.url
            if int(curPage) < int(totalPage):
                urlfragments = response.url.split("/")
                curPageadd = str(int(curPage) + 1)
                if 'pg' in urlNow:
                    nextUrl = urlNow.replace('pg%s' % curPage, 'pg%s' % curPageadd)
                else:
                    nextUrl = urlfragments[0] + '//' + urlfragments[2] + '/' + urlfragments[3] + '/pg%s' % curPageadd + urlfragments[4] + '/'
                try:
                    logger.info("爬取房源的下一页" + nextUrl)
                    yield scrapy.Request(nextUrl, callback=self.parse)
                    # time.sleep(random.randint(3, 8))
                except:
                    logger.error("房源爬取下一页出错" + nextUrl)
            else:
                print("===========================")
                if 'pg' in urlNow:
                    urlNow = urlNow.replace('pg%s' % curPage, '')

                # 当该商圈的所有房源爬取完成后将相应的标志设为1，目的是断点续爬的实现
                sql = "UPDATE lianjiaCommunityInfo SET visited=1 WHERE rentUrl='%s';" % urlNow
                db.updateSql(sql)
                logger.info("一条小区链接爬取完成" + response.url)
        else:
            logger.info('该小区没有租房信息' + response.url)
            urlNow = response.url
            sql = "UPDATE lianjiaCommunityInfo SET visited=2 WHERE rentUrl='%s';" % urlNow
            db.updateSql(sql)
            logger.info("一条没有租房信息的小区链接爬取完成" + response.url)
            pass

