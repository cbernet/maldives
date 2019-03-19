import scrapy

class LeboncoinSpider(scrapy.Spider):
    name = 'leboncoin'
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:10.0) Gecko/20100101 Firefox/10.0"
        
    def start_requests(self):
        urls = ['https://www.leboncoin.fr/ventes_immobilieres/offres/']
        for url in urls: 
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        print(response.url)