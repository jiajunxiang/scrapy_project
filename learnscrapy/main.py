#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/2/25 13:44
import pymysql
from scrapy.cmdline import execute

if __name__ == '__main__':
    execute(['scrapy', 'crawl', 'ssr3'])
    # conn=pymysql.connect(
    #         host='localhost',
    #         user='root',
    #         password='123456',
    #         db='test',
    #         port=3306,
    #         charset='utf8',
    #          # 自动二次确认
    #         autocommit=True)
    # try:
    #     if conn.open:
    #         print('success')
    #     with conn.cursor() as cursor:
    #         sql = "insert into movie(title,fraction,time,country,director,date) values ('1','33','3','4','5','6')"
    #         cursor.execute(sql)
    #         version = cursor.fetchone()
    #         print(version)
    # except pymysql.MySQLError as e:
    #     print(f'失败:{e}')
    # finally:
    #     conn.close()