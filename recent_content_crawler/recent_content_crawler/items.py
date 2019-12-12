# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy_djangoitem
from scrapy_djangoitem import DjangoItem, Field
from crawler_model.models import recent_content


class RecentContentCrawlerItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model=recent_content

    
