# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
# useful for handling different item types with a single interface


class LearnscrapyPipeline:

    def __init__(self):
        self.conn:pymysql.connect
        self.cur:pymysql.cursors.Cursor
        self.queue = []
        self.count = 0

    def connect_db(self):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            db='test',
            port=3306,
            charset='utf8')
        self.cur = self.conn.cursor()

    def close_db(self):
        if len(self.queue) > 0:
            self.insert_data()
        self.cur.close()
        self.conn.close()

    def insert_data(self):
        self.connect_db()
        sql = ("insert into spa5"
               "(title,author,price,time,press,page,isbm) "
               "values (%s,%s,%s,%s,%s,%s,%s)")
        self.cur.executemany(sql, self.queue)
        self.queue.clear()
        self.conn.commit()
        self.close_db()

    def process_item(self, content, spider):
        self.queue.append(
            (content['title'], content['author'], content['price'],
             content['time'], content['press'], content['page'],content['isbm']))
        if len(self.queue) > 30:
            # print(self.queue)
            self.insert_data()
        return content

    # def process_item(self, content, spider):
    #     # print(content)
    #     return content
