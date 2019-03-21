import scrapy
import time 
import pprint

class SelogerSpider(scrapy.Spider):
    name = 'seloger'
        
    def start_requests(self):
        url = 'https://www.seloger.com/list.htm?types=1%2C2&projects=2%2C5&enterprise=0&natures=1%2C2%2C4&places=%5B%7Bci%3A690123%7D%5D&qsVersion=1.0'
        i=1
        imax=1
        while 1:
            if i==imax+1:
                break
            pageurl = url+'&LISTING-LISTpg='+str(i)
            i+=1
            yield scrapy.Request(url=pageurl, callback=self.parse)
            
            
    def parse(self, response):
        # print(response.url)
        links = response.css('div.c-pa-info a.c-pa-link::attr(href)').getall()
        # pprint.pprint(links)
        for link in links: 
            adpage = response.urljoin(link)
            yield scrapy.Request(adpage, callback=self.parse_ad)
            
    def parse_ad(self, response):
        items = response.css('div.c-slice').css('ul.criterion li::text').getall()
        results = dict()
        for item in items: 
            key, val = item.split()
            results[key] = val
        return results
    