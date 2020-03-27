from scrapy import cmdline

# cmdline.execute('scrapy crawl lianjia_crawler -o data.csv -t csv'.split())
# cmdline.execute('scrapy crawl lianjia_crawler '.split())

# 爬取商圈链接共241条
# cmdline.execute('scrapy crawl lianjia_shopping '.split())
# 根据商圈链接爬取小区信息
cmdline.execute('scrapy crawl lianjia_community '.split())
