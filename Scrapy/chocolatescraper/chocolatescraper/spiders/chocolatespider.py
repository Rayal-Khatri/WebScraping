import scrapy
import re
from chocolatescraper.items import ChocolateProduct
from chocolatescraper.itemsloader import ChocolateProductLoader 


class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):
        products = response.css(".product-item")

        for product in products:
            chocolate = ChocolateProductLoader(item = ChocolateProduct(), selector= product)

            chocolate.add_css('name', "a.product-item-meta__title::text")

            price_text = ''.join(product.css('span.price *::text').getall()).strip()
            price = re.search(r'£\d+\.?\d*', price_text).group()
            chocolate.add_value('price', price)

            chocolate.add_css('url', ".product-item-meta a::attr(href)")
            yield chocolate.load_item()

        next_page = response.css('[rel="next"]::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://www.chocolate.co.uk' + next_page 
            yield response.follow(next_page_url,callback = self.parse)