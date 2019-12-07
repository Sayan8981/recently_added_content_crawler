import scrapy 
from scrapy import *
import sys
import os
#import pdb;pdb.set_trace()
sys.path.insert(0,os.getcwd()+'/xpath')
import xpath

class instantwatcherbrowse(Spider):

    name="recently_added"
    start_urls=["https://instantwatcher.com"]

    def __init__(self):
        self.content_type_key=[]

    def parse(self,response):
        #import pdb;pdb.set_trace()
        sel=Selector(response)
        source_node=sel.xpath(xpath.source_node).extract()
        print(source_node)
        #import pdb;pdb.set_trace() 
        for source in source_node:
            if source.lower()== "amazon":
                #import pdb;pdb.set_trace()  
                amazon_url=''.join(sel.xpath(xpath.amazon_url_xpath%source).extract())
                yield Request(url=''.join(self.start_urls)+amazon_url,meta={'source_name':source},
                                                  callback=self.parse_url,dont_filter = True)

        
    def parse_url(self,response):
        #import pdb;pdb.set_trace()
        provider_name=response.meta['source_name']
        section=response.xpath(xpath.section_xpath%response.meta['source_name']).extract()
        section_url=response.xpath(xpath.section_urls%response.meta['source_name']).extract()
        source_section_wise_url=dict(zip(section,section_url))
        print(source_section_wise_url)
        if provider_name=='Amazon':
            yield Request(url=''.join(self.start_urls)+source_section_wise_url["New Prime"]
                                                   ,callback=self.parse_amazon_content,dont_filter=True)

    def parse_amazon_content(self,response):
        #import pdb;pdb.set_trace()
        #print (response.body)
        content_type=response.xpath(xpath.checked_content_type_xpath).extract()[1:]
        for content in content_type:
            self.content_type_key.append(''.join(response.xpath(xpath.checked_content_type_key_xpath%content).extract()))
        dict_content_type_key=dict(zip(content_type,self.content_type_key))
        for key,value in dict_content_type_key.items():
            content_url=response.url.replace('1+2','%s'%value)
            yield Request(url=content_url,meta={'content_type':key},callback=self.content_scraped,dont_filter=True)

    def content_scraped(self,response):
        print ([response.url,response.meta["content_type"]])        