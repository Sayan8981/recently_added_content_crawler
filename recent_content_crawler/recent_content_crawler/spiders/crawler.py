import scrapy 
from scrapy import *
import sys
import os
from datetime import datetime,timedelta
from recent_content_crawler.items import *
sys.path.insert(0,os.getcwd()+'/xpath')
import xpath

class instantwatcherbrowse(Spider):

    name="recently_added"
    start_urls=["https://instantwatcher.com"]

    def __init__(self):
        self.content_type_key=[]
        self.amazon_url=''
        self.provider_name=''
        
    def parse(self,response):
        #import pdb;pdb.set_trace()
        sel=Selector(response)
        source_node=sel.xpath(xpath.source_node).extract()
        print(source_node)
        #import pdb;pdb.set_trace() 
        for source in source_node:
            if source.lower()== "amazon":
                #import pdb;pdb.set_trace()  
                self.amazon_url=''.join(sel.xpath(xpath.amazon_url_xpath%source).extract())
                yield Request(url=''.join(self.start_urls)+self.amazon_url,meta={'source_name':source},
                                                  callback=self.parse_url,dont_filter = True)

        
    def parse_url(self,response):
        #import pdb;pdb.set_trace()
        self.provider_name=response.meta['source_name']
        section=response.xpath(xpath.section_xpath%response.meta['source_name']).extract()
        section_url=response.xpath(xpath.section_urls%response.meta['source_name']).extract()
        source_section_wise_url=dict(zip(section,section_url))
        print(source_section_wise_url)
        if self.provider_name=='Amazon':
            yield Request(url=''.join(self.start_urls)+source_section_wise_url["New Prime"]
                                   ,meta={"service":"New Prime"}
                                      ,callback=self.parse_amazon_content,dont_filter=True)

    def parse_amazon_content(self,response):
        #import pdb;pdb.set_trace()
        content_type=response.xpath(xpath.checked_content_type_xpath).extract()[1:]
        for content in content_type:
            self.content_type_key.append(''.join(response.xpath(xpath.checked_content_type_key_xpath%content).extract()))
        dict_content_type_key=dict(zip(content_type,self.content_type_key))
        for key,value in dict_content_type_key.items():
            content_url=response.url.replace('1+2','%s'%value)
            yield Request(url=content_url,meta={'content_type':key,"service":response.meta["service"]}
                                                               ,callback=self.pagination,dont_filter=True)

    def pagination(self,response):
        #import pdb;pdb.set_trace()
        if self.provider_name=='Amazon':
            if response.meta["content_type"].lower() == 'movies':
                yield Request(url=response.url,meta={"content_type":response.meta["content_type"],
                               "service":response.meta["service"]},callback=self.content_scraped,dont_filter=True)
                #import pdb;pdb.set_trace()
                next_page_url="{}{}{}{}".format(''.join(self.start_urls),self.amazon_url,'/search',''.join(response.xpath(xpath.next_page).extract()))
                if next_page_url is not None:
                    if next_page_url !="{}{}{}".format(''.join(self.start_urls),self.amazon_url,'/search'):
                        yield Request(url=next_page_url,meta={"content_type":response.meta["content_type"],
                              "service":response.meta["service"]},callback=self.pagination,dont_filter=True)
            
    def content_scraped(self,response):
        #import pdb;pdb.set_trace()
        item=RecentContentCrawlerItem()
        
        sel=Selector(response)
        print ("\n")
        print ([response.url,response.meta["content_type"]])
        require_date=(datetime.now() - timedelta(days=1)).strftime('%b %d, %Y')

        title_array=sel.xpath(xpath.title_xpath%require_date).extract()
        for title in title_array:
            item["title"]=title
            if response.meta["content_type"].lower()=='movies':
                item["Show_type"]='MO'
            item["Source"]=self.provider_name
            item["Service"]=response.meta["service"]
            item["content_type"]='Recently_Added'
            item["Added_to_site"]=require_date
            item["Updated_at_DB"]=datetime.now().strftime('%b %d, %Y')  
            print (item)
            yield item
        
           