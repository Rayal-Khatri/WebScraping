import scrapy
import re

class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):
        products = response.css(".product-item")
        for product in products:
            yield{
                'title' : product.css("a.product-item-meta__title::text").get(),
                'price' : re.search(r'£\d+\.?\d*',product.css('span.price::text').getall()[-1].strip()).group(),
                'url' : product.css("a.product-item-meta__title").attrib['href'],
            }

        next_page = response.css('[rel="next"]::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://www.chocolate.co.uk' + next_page 
            yield response.follow(next_page_url,callback = self.parse)