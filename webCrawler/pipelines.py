# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class WebcrawlerPipeline(object):
    def process_item(self, item, spider):
        f = self.file('data.csv', 'a+')
        writer = csv.writer(f)
        writer.writerow((item['houseUrl'], item['price'], item['area'],
                         item['houseType'], item['towards'], item['address'],
                         item['regional'], item['time'], item['shopping'],
                         item['community'], item['floor']))
        return item
