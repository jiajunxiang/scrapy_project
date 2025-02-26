# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LearnscrapyItem(scrapy.Item):
    # define the fields for your item here like:

    # 影片名字
    title = scrapy.Field()
    # 影片分数
    fraction=scrapy.Field()
    # 上映时间
    date=scrapy.Field()
    # 发行地区
    country=scrapy.Field()
    # 影片时长
    time=scrapy.Field()
    # 影片导演
    director=scrapy.Field()