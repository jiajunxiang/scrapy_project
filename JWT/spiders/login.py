#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/2/25 13:43
# 含有jwt参数的页面
import scrapy
from scrapy import Request
from learnscrapy.items import BookscrapyItem


class Ssr1Spider(scrapy.Spider):
    name = "login"
    jwt = ''
    offset = 0
    limit = 18
    base_url = 'https://login3.scrape.center/api/book/'
    urls = base_url + f'?limit={limit}&offset=%s'
    # 覆盖全局设置中的设置，使用自定义的下载中间件
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'learnscrapy.middlewares.DIYDownloaderMiddleware': 543,
        }
    }

    def start_requests(self):
        param={
            'username':'admin',
            'password':'admin'
        }
        # 添加需要提交的表单参数
        yield scrapy.FormRequest(url='https://login3.scrape.center/api/login',callback=self.parse,formdata=param)

    def parse(self, response,**kwargs):
        result = response.json()
        # 从响应中获取到 jwt
        if 'token' in result:
            self.jwt = result['token']
        # 从起始页面开始爬取
        yield scrapy.Request(url=self.urls % self.offset, callback=self.parse_page)

    def parse_page(self,response):
        print(response.url)
        result=response.json()
        for item in result['results']:
            content=BookscrapyItem()
            content['title']=item['name']
            ls_author = []
            for i in (item['authors'] or []):
                ls_author.append(i.strip())
            str_result='/'.join(ls_author)
            content['author']=str_result
            # content['author']= '/'.join([c.strip() for c in (item['authors'] or [])])
            yield scrapy.Request(url=self.base_url+f'{item['id']}/', callback=self.parse_childPage,meta={'content':content})
        if int(result['count']) > self.offset:
            self.offset += self.limit
            yield Request(url=self.urls % self.offset, callback=self.parse_page)


    def parse_childPage(self, response):
        content = response.meta['content']
        result = response.json()
        content['price'] = result['price'] or 0
        content['time'] = result['published_at']
        content['press'] = result['publisher']
        content['page'] = result['page_number']
        content['isbm'] = result['isbn']
        yield content
