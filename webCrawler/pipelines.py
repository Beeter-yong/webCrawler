# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from webCrawler.utils.mysqlUtil import database
from webCrawler.utils.logger import Logger
logger = Logger(name='pipeline')


class DownShoppingUrlPipeline(object):
    # 向数据库存储商圈链接
    def open_spider(self,spider):
        self.connect = pymysql.connect(
            host='39.97.225.8',  # 数据库地址
            port=3306,  # 数据库端口
            db='rentData',  # 数据库名
            user='root',  # 数据库用户名
            passwd='123456',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        sql_select = "select * from lianjiaShoppingUrl where shopingUrl='%s';" % (item['shopingUrl'])
        rows = self.cursor.execute(sql_select)
        if rows != 0:
            print('此商圈链接已经存在-----------------')
            pass
        else:
            sql_add = "insert into lianjiaShoppingUrl(shopingUrl, shopingName, shopingRegitional) values (%s, %s, %s);"
            try:
                # 没有异常对数据库进行提交
                self.cursor.execute(sql_add, (item['shopingUrl'], item['shopingName'], item['shopingRegitional']))
                self.connect.commit()
            except Exception as e:
                # 有异常对数据库进行回滚
                print(e)
                self.connect.rollback()
            return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()


class DownCommunityInfoPipeline(object):
    # 向数据库存储小区信息
    def open_spider(self, spider):
        self.db = database()

    def process_item(self, item, spider):
        sql_select = "select * from lianjiaCommunityInfo where communityUrl='%s';" % (item['communityUrl'])
        result = self.db.selectSql(sql_select)
        if result:
            logger.info("此小区已经记录在数据库中" + item['communityUrl'])
            pass
        else:
            sql_add = "insert into lianjiaCommunityInfo(communityUrl, communityName, regional, shopping, communityImg, rentUrl, buildingTime, buildingType, propertyName, propertyFees, developer, buildingNum, houseingNum, nearbyStores, tag) " \
                      "values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' );"%(
                item['communityUrl'], item['communityName'], item['regional'], item['shopping'], item['communityImg'],
                item['rentUrl'], item['buildingTime'], item['buildingType'], item['propertyName'], item['propertyFees'],
                item['developer'], item['buildingNum'], item['houseingNum'], item['nearbyStores'], item['tag']
            )
            self.db.insertSql(sql_add)
            return item

    def close_spider(self, spider):
        self.db.close()

class DownRentInfoPipeline(object):
    # 向数据库存储租房房源信息
    def open_spider(self, spider):
        self.db = database()

    def process_item(self, item, spider):
        sql_select = "select * from lianjiaRentInfo where houseUrl='%s';" % (item['houseUrl'])
        result = self.db.selectSql(sql_select)
        if result:
            logger.info("此房源信息已经记录在数据库中" + item['houseUrl'])
            pass
        else:
            sql_add = "insert into lianjiaRentInfo(houseUrl, price, area, houseType, towards, address, regional, shopping, community, floor, timeLast, timeNew, rentImg) " \
                      "values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
                          item['houseUrl'], item['price'], item['area'], item['houseType'],
                          item['towards'],
                          item['address'], item['regional'], item['shopping'], item['community'],
                          item['floor'],
                          item['time'], item['timeNew'], item['rentImg']
                      )
            self.db.insertSql(sql_add)
            return item

    def close_spider(self, spider):
        self.db.close()
