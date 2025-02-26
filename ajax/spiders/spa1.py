#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/2/25 13:43
# 页面直接内嵌在网页源代码中
import scrapy
from scrapy import Request
from learnscrapy.items import LearnscrapyItem


class Ssr1Spider(scrapy.Spider):
    name = "spa1"
    # # 覆盖全局设置中的设置，使用自定义的下载中间件,进行身份验证
    # custom_settings = {
    #     'DOWNLOADER_MIDDLEWARES': {
    #         'learnscrapy.middlewares.DIYDownloaderMiddleware': 543,
    #     }
    # }
    allowed_domains = ["spa1.scrape.center"]
    start_urls = ["https://spa1.scrape.center/"]

    def start_requests(self):
        urls=[f'https://spa1.scrape.center/api/movie/?limit=10&offset={num}' for num in range(0,100,10)]
        for url in urls:
            yield Request(url=url,callback=self.parse)


    def parse(self, response,**kwargs):
        contents=response.json()
        for item in contents['results']:
            content=LearnscrapyItem()
            content['title']=item['name']+item['alias']
            content['fraction']='、'.join(item['categories'])
            content['country']='和'.join(item['regions'])
            content['time']=item['minute']
            content['date']=item['published_at']
            # 影片导演在子页面，需要单独进行处理
            yield Request(url=response.urljoin(f'/api/movie/{item['id']}/'),callback=self.parse_director,meta={'content':content})
    def parse_director(self,response):
        result=response.json()
        content=response.meta['content']
        content['director']=result['directors'][0]['name']
        yield content
