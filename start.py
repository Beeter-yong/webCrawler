from scrapy import cmdline

# cmdline.execute('scrapy crawl lianjia_crawler -o data.csv -t csv'.split())
# cmdline.execute('scrapy crawl lianjia_crawler '.split())

cmdline.execute('scrapy crawl lianjia_community '.split())
