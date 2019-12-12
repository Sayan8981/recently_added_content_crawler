import scrapy 
from scrapy import *
import sys
import os
import time
from datetime import datetime,timedelta
from recent_content_crawler.items import *
sys.path.insert(0,os.getcwd()+'/xpath')
import xpath

class instantwatcherbrowse(Spider):

    name="recently_added"
    start_urls=["https://instantwatcher.com"]

    #initialization:
    def __init__(self):
        self.content_type_key=[]
        self.source_url=''
        self.provider_name=''
        self.title_array_prev_dates=[]
        self.require_date=''
        self.all_title_array=[]

    def cleanup(self):
        self.all_title_array=[]    
        self.title_array_prev_dates=[]
        self.content_type_key=[]

    def parse(self,response):
        #import pdb;pdb.set_trace()
        sel=Selector(response)
        source_node=sel.xpath(xpath.source_node).extract()
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36',
            'Sec-Fetch-User': '?1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8,la;q=0.7',
        }
        #import pdb;pdb.set_trace() 
        for source in source_node:
            if source.lower()== "amazon":
                #import pdb;pdb.set_trace()  
                self.source_url=''.join(sel.xpath(xpath.source_url_xpath%source).extract())
                yield Request(url=''.join(self.start_urls)+self.source_url,meta={'source_name':source},
                                        headers=headers,callback=self.parse_url,dont_filter = True)

        
    def parse_url(self,response):
        #import pdb;pdb.set_trace()
        self.provider_name=response.meta['source_name']
        section=response.xpath(xpath.section_xpath%response.meta['source_name']).extract()
        section_url=response.xpath(xpath.section_urls%response.meta['source_name']).extract()
        source_section_wise_url=dict(zip(section,section_url))
        if self.provider_name=='Amazon':
            yield Request(url=''.join(self.start_urls)+source_section_wise_url["New Prime"]
                                   ,meta={"service":"New Prime"}
                                      ,callback=self.parse_amazon_content,dont_filter=True)

    def parse_amazon_content(self,response):
        #import pdb;pdb.set_trace()
        print (response.body)
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
                               "service":response.meta["service"]},callback=self.call_next_page,dont_filter=True)
            else:
                yield Request(url=response.url,meta={"content_type":response.meta["content_type"],
                               "service":response.meta["service"]},callback=self.call_next_page,dont_filter=True)


    def call_next_page(self,response):
        yield Request(url=response.url,meta={"content_type":response.meta["content_type"],
                       "service":response.meta["service"]},callback=self.content_scraped,dont_filter=True)
        #import pdb;pdb.set_trace()
        next_page_url="{}{}{}{}".format(''.join(self.start_urls),self.source_url,'/search',''.join(response.xpath(xpath.next_page).extract()))
        if next_page_url is not None:
            if next_page_url !="{}{}{}".format(''.join(self.start_urls),self.source_url,'/search'):
                yield Request(url=next_page_url,meta={"content_type":response.meta["content_type"],
                      "service":response.meta["service"]},callback=self.pagination,dont_filter=True)                              
            
    def content_scraped(self,response):
        #import pdb;pdb.set_trace()
        self.cleanup()
        sel=Selector(response)
        self.require_date=(datetime.now() - timedelta(days=1)).strftime('%b %d, %Y')
        date_node=sel.xpath('//h4/text()').extract()
        import pdb;pdb.set_trace()  
        if len(date_node)>1:
            for date in date_node:
                if date==self.require_date:
                    self.all_title_array=sel.xpath(xpath.title_xpath%str(date)).extract()
                else:
                    self.title_array_prev_dates=sel.xpath(xpath.title_xpath%str(date)).extract()
            title_array=list(set(self.all_title_array)-set(self.title_array_prev_dates))
            if title_array:
                yield Request(url=response.url,meta={"title_array":title_array,"content_type":response.meta["content_type"],
                          "service":response.meta["service"]},callback=self.item_stored,dont_filter=True)
        else:
            title_array=sel.xpath(xpath.title_xpath%self.require_date).extract()
            if title_array:
                yield Request(url=response.url,meta={"title_array":title_array,"content_type":response.meta["content_type"],
                          "service":response.meta["service"]},callback=self.item_stored,dont_filter=True)


    def item_stored(self,response): 
        import pdb;pdb.set_trace()
        for title in response.meta["title_array"]:
            item=RecentContentCrawlerItem()
            item["title"]=str(title)
            if response.meta["content_type"].lower()=='movies':
                item["Show_type"]='MO'
            else:
                item["Show_type"]='TVSeason'    
            item["Source"]=self.provider_name
            item["Service"]=response.meta["service"]
            item["content_type"]='Recently_Added'
            item["Added_to_site"]=self.require_date
            item["Updated_at_DB"]=datetime.now().strftime('%b %d, %Y') 
            print ("\n") 
            print ("Crawling ....",item["Updated_at_DB"])
            yield item             
                    
        
           