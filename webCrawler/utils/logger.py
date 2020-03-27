import logging

class Logger:
    def __init__(self, name='myLog', path='myLog.log', level='INFO'):
        """
        创建一个log日志
        :param name: 指定log名字，同一个名字使用的相同的log实例
        :param path: 指定log文件的路径
        :param level: 指定log的级别
        """
        # 创建一个logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(path, encoding='utf-8')
        fh.setLevel(level)
        # 再创建一个handler，用于输出控制台
        ch = logging.StreamHandler()
        ch.setLevel(level)
        # 定义handler的输出方式
        formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


if __name__ == '__main__':
    logger = Logger()
    logger.info("nihao")
