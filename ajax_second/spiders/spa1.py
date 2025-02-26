#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/2/25 13:43
# 页面没有初始的url，通过Ajax滑动到底部自动刷新下一页数据
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
    allowed_domains = ["spa3.scrape.center"]
    start_urls = ["https://spa3.scrape.center/"]

    offset=0
    index_url = f'https://spa3.scrape.center/api/movie/?limit=10&offset=%s'

    def start_requests(self):
        urls=[self.index_url % self.offset]
        for url in urls:
            # print(url)
            yield Request(url=url,callback=self.parse)


    def parse(self, response,**kwargs):
        contents=response.json()
        for item in contents['results']:
            # 越界返回空数据过滤
            if item['id'] > contents['count']:
                continue
            content=LearnscrapyItem()
            content['title']=item['name']+item['alias']
            content['fraction']='、'.join(item['categories'])
            content['country']='和'.join(item['regions'])
            content['time']=item['minute']
            content['date']=item['published_at']
            # 影片导演在子页面，需要单独进行处理
            yield Request(url=response.urljoin(f'/api/movie/{item['id']}/'),callback=self.parse_director,meta={'content':content})
        if self.offset < contents['count']:
            # 因为每次请求限制10条数据，所以每次将偏移量+10
            self.offset += 10
            print(self.index_url % self.offset)
            yield Request(url=self.index_url % self.offset, callback=self.parse)

    def parse_director(self,response):
        result=response.json()
        content=response.meta['content']
        content['director']=result['directors'][0]['name']
        yield content
