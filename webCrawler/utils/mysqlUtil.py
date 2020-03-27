import pymysql
from webCrawler.utils.logger import Logger

logger = Logger(name='mysql')

class database:
    # 数据库连接
    def __init__(self):
        try:
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
            logger.info("数据库连接成功")
        except:
            logger.critical("数据库连接失败")

    # 数据库关闭
    def close(self):
        try:
            self.cursor.close()
            self.connect.close()
            logger.info("数据库关闭")
        except:
            logger.critical("未创建数据库连接就关闭")

    # 传入SQL语句查询数据库并返回元组结果
    def selectSql(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            logger.info("执行查询语句---" + sql)
            return result
        except Exception as e:
            logger.error("数据库查询出错" + e)

    # 传入SQL语句更新数据库
    def updateSql(self, sql):
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            logger.info("执行更新操作---" + sql)
        except Exception as e:
            logger.error("数据库更新错误" + e)
            self.connect.rollback()
