#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/2/25 13:43
# 页面直接内嵌在网页源代码中
import scrapy
from scrapy import Request
from learnscrapy.items import LearnscrapyItem


class Ssr1Spider(scrapy.Spider):
    name = "ssr3"
    # # 覆盖全局设置中的设置，使用自定义的下载中间件,进行身份验证
    # custom_settings = {
    #     'DOWNLOADER_MIDDLEWARES': {
    #         'learnscrapy.middlewares.DIYDownloaderMiddleware': 543,
    #     }
    # }
    allowed_domains = ["ssr4.scrape.center"]
    start_urls = ["https://ssr4.scrape.center/"]

    def start_requests(self):
        urls=[f'https://spa1.scrape.center/api/movie/?limit=10&offset={num}' for num in range(0,100,10)]
        for url in urls:
            yield Request(url=url,callback=self.parse)
        # yield Request(url="https://ssr1.scrape.center/page/2", callback=self.parse)


    def parse(self, response,**kwargs):
        table_items=response.xpath('//div[@class="el-card item m-t is-hover-shadow"]')
        for item in table_items:
            content=LearnscrapyItem()
            content['title']=item.xpath('.//h2[@class="m-b-sm"]/text()').get()
            content['fraction']=item.xpath('//p[@class="score m-t-md m-b-n-sm"]/text()').get().strip()
            content['country']=item.xpath('.//div[@class="m-v-sm info"]/span[1]/text()').get()
            content['time']=item.xpath('.//div[@class="m-v-sm info"]/span[3]/text()').get()
            content['date']=item.xpath('.//div[@class="m-v-sm info"][2]/span/text()').get()
            url=item.xpath('.//a[@class="name"]/@href').get()
            # 影片导演在子页面，需要单独进行处理
            yield Request(url=response.urljoin(url),callback=self.parse_director,meta={'content':content})
    def parse_director(self,response):
        content=response.meta['content']
        content['director']=response.xpath('//div[@class="directors el-row"]//p[@class="name text-center m-b-none m-t-xs"]/text()').get()
        yield content
