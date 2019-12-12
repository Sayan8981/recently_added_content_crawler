# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import os

class RecentContentCrawlerPipeline(object):

    def __init__(self):
        self.counter=0

    def process_item(self, item, spider):
        self.counter+=1
        print ("commited...","count:",self.counter)
        print ("\n")
        item.save()
        return item
