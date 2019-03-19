import scrapy
import time 
import pprint

class SelogerSpider(scrapy.Spider):
    name = 'seloger'
        
    def start_requests(self):
        url = 'https://www.seloger.com/list.htm?types=1%2C2&projects=2%2C5&enterprise=0&natures=1%2C2%2C4&places=%5B%7Bci%3A690123%7D%5D&qsVersion=1.0'
        i=1
        imax=10
        while 1:
            if i==imax:
                break
            pageurl = url+'&LISTING-LISTpg='+str(i)
            i+=1
            yield scrapy.Request(url=pageurl, callback=self.parse)
            
            
    def parse(self, response):
        time.sleep(1)
        print(response.url)
        links = response.css('div.c-pa-info a.c-pa-link::attr(href)').getall()
        pprint.pprint(links)