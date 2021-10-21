# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql as pymysql
from itemadapter import ItemAdapter

from ybj.settings import *


class YbjPipeline:
    def open_spider(self, spider):
        # 爬虫项目启动，执行连接数据操作
        # 以下常量需要定义在settings配置文件中
        self.db = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PWD,
            database=MYSQL_DB,
            charset=MYSQL_CHARSET
        )
        self.cursor = self.db.cursor()

    # 向表中插入数据
    def process_item(self, item, spider):
        ins = 'INSERT INTO `t_file` (`title`,`content`,`url`) VALUES(%s,%s,%s)'
        L = [item['title'], item['content'], item['url']]

        self.cursor.execute(ins, L)
        self.db.commit()
        return item

    # 结束存放数据，在项目最后一步执行
    def close_spider(self, spider):
        # close_spider()函数只在所有数据抓取完毕后执行一次，
        self.cursor.close()
        self.db.close()
        print('执行了close_spider方法,项目已经关闭')
