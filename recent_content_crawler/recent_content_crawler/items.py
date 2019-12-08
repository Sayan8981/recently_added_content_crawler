# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RecentContentCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    Show_type=scrapy.Field()
    Source=scrapy.Field()
    Service=scrapy.Field()
    content_type=scrapy.Field()
    Added_to_site=scrapy.Field()
    Updated_at_DB=scrapy.Field()
    
