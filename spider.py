#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-04-01 16:32:27
# Project: tripadvisor

from pyspider.libs.base_handler import *
import pymongo


client = pymongo.MongoClient('localhost')
db = client['tripadvisor']

client = pymongo.MongoClient('localhost')
db = client['tripadvisor']
my_set = db['los_angeles']


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.tripadvisor.cn/Attractions-g32655-Activities-Los_Angeles_California.html', callback=self.index_page, validate_cert = False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('#ATTR_ENTRY_ > div.attraction_clarity_cell > div > div > div.listing_info > div.listing_title > a').items():
            self.crawl(each.attr.href, callback=self.detail_page, validate_cert = False)
            next = response.doc('.pagination .nav.next').attr.href #翻到下一页
            self.crawl(next, callback = self.index_page, validate_cert = False)#每一页回调之后，又把下一页的链接回调
    
    
    @config(priority=2)
    def detail_page(self, response):
        url = response.url
        name = response.doc('#HEADING').text()
        address = response.doc('.location > .address').text()
            
       
        data =    {
            "url": url,
            "name": name,
            "address": address
        }
        my_set.insert(data)）#存到mongodb
        return(data)
     

        
    
    

    
    
    
    
    
    


             
    
    
    
    
    
