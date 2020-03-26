# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import pymysql

class MysqlPipeline(object):
    # 向数据库存储租房信息
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
        sql_select = "select * from lianjia where houseUrl='%s';" % (item['houseUrl'])
        rows = self.cursor.execute(sql_select)

        if rows != 0:
            print('此数据已经存在-----------------')
            pass
        else:
            sql_add = """
            insert into lianjia(houseUrl, price, area, houseType, towards, address, regional, shopping, community, floor, timeLast) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            try:
                # 无异常数据库提交
                self.cursor.execute(sql_add, (
                    item['houseUrl'], item['price'], item['area'], item['houseType'], item['towards'],
                    item['address'], item['regional'], item['shopping'], item['community'], item['floor'],
                    item['time']
                ))
                self.connect.commit()
            except Exception as e:
                # 有异常对数据库进行回滚
                print(e)
                self.connect.rollback()
            return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

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