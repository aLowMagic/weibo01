# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Weibo01TextItem(scrapy.Item):
    picture = scrapy.Field()
    userid = scrapy.Field()
    url_id = scrapy.Field()
    content = scrapy.Field()
    picsUrl = scrapy.Field()
    picStr = scrapy.Field()
    source_id = scrapy.Field()