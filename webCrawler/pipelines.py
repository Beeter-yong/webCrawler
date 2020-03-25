# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import pymysql

class MysqlPipeline(object):
    def __init__(self):
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
        sql = """
        insert into lianjia(houseUrl, price, area, houseType, towards, address, regional, shopping, community, floor, timeLast) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (
            item['houseUrl'], item['price'], item['area'], item['houseType'], item['towards'],
            item['address'], item['regional'], item['shopping'], item['community'], item['floor'],
            item['time']
        ))
        self.connect.commit()
        return item
    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

