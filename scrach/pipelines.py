# -*- coding: utf-8 -*-
from scrapy import signals
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
import json

class ScrachPipeline(object):
    #def __init__(self):
    #    self.file = codecs.open('date.json','w',encoding='utf-8') 
    #    self.file.write('[')
    # def process_item(self, item, spider):
    # 	# line = json.dumps(dict(item)) + ','
    # 	# self.file.write(line.decode("unicode_escape"))
    #     #return item
    #     line = json.dumps(dict(item), ensure_ascii=False) + "\n"
    #     self.file.write(line)
    #     return item

    # def close_spider(self, spider):
    #     #self.file.seek(-1, os.SEEK_END)
    #     #self.file.truncate();
    #     self.file.write(']')
    #     self.file.close()

    # @classmethod
    # def from_crawler(cls, crawler):
    #      pipeline = cls()
    #      crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
    #      crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
    #      return pipeline

    # def spider_opened(self, spider):
    #     self.file = open('date.json', 'wb')
    #     self.exporter = JsonItemExporter(self.file,ensure_ascii=False)
    #     self.exporter.start_exporting()

    # def spider_closed(self, spider):
    #     self.exporter.finish_exporting()
    #     self.file.close()

    # def process_item(self, item, spider):
    #     self.exporter.export_item(item)
    #     return item

    #插入的sql语句
    jxrdate_key = ['content','tid','title','images','flag','author']
    insertJxrdate_sql = '''insert into jxrdate (%s) values (%s)'''
    jxrdate_query_sql = "select tid from jxrdate where tid = (%s)"
    max_dropcount = 50
    current_dropcount = 0

    def __init__(self):
        dbargs = settings.get('DB_CONNECT')
        db_server = settings.get('DB_SERVER')
        dbpool = adbapi.ConnectionPool(db_server,**dbargs)
        self.dbpool = dbpool

    def __del__(self):
        self.dbpool.close()

    #处理每个item并返回
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        return item

    #插入数据
    def _conditional_insert(self, tx, item):
        #重复插入查询
        tx.execute(self.jxrdate_query_sql,(item['tid'],))
        result = tx.fetchone()
        if result == None:
            self.insert_data(item,self.insertJxrdate_sql,self.jxrdate_key)

    #插入数据到数据库中
    def insert_data(self, item, insert, sql_key):
        fields = u','.join(sql_key)
        qm = u','.join([u'%s'] * len(sql_key))
        sql = insert % (fields,qm)
        data = [item[k] for k in sql_key]
        return self.dbpool.runOperation(sql,data)
