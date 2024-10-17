import scrapy
import scrapy.responsetypes
from scrapy import FormRequest

from quotestoscrape.items import QuoteItem


class LoginSpider(scrapy.Spider):
    name = "Login_Spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/login"]

    def parse(self, response):
        pass

    def start_requests(self):
        login_url = 'https://quotes.toscrape.com/login'
        yield scrapy.Request(login_url, callback=self.login)

    def login(self, response):
        token = token = response.css('input[name="csrf_token"]').xpath('@value').get()
        if not token:
            self.logger.error("CSRF token not found!")
            return
        self.logger.info("Attempting to log in...")
        
        return FormRequest.from_response(response, formdata={
            'csrf_token': token,
            'username': "jpt@jpt.com",
            'password': "123456789"
        }, callback=self.start_scraping)


    def start_scraping(self,response):
            print("************************************************************************")
            print(response.css('.header-box .col-md-4 a::text').get())
            for quote in response.css('div.quote'):
                quote_item = QuoteItem()
                quote_item['text'] = quote.css("span.text::text").get()
                quote_item['author'] = quote.css("small.author::text").get()
                quote_item['tags']= quote.css("a.tag::text").get()
                yield quote_item

            next_page= response.css('.next a').xpath('@href').get()
            if next_page is not None:
                next_page_url = "https://quotes.toscrape.com" + next_page
                yield scrapy.Request(url=next_page_url, callback = self.parse)