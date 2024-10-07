import scrapy


class DarazspiderSpider(scrapy.Spider):
    name = "darazspider"
    allowed_domains = ["daraz.com.np",'pages.daraz.com.np']
    start_urls = ["https://pages.daraz.com.np/"]

    def parse(self, response):
        products = products = response.css('.card-fs-content-body a.card-fs-content-body-unit')
        for product in products:
            yield{
                'title' : product.css('.fs-card-text p.fs-card-title::text').get(),
                'Price':  product.css('.fs-card-text .fs-card-price span.price::text').get(),
                'Discount' :  product.css('.fs-card-text .fs-card-origin-price span.itemDiscount::text').get()
                }
            
