from typing import Iterable
import scrapy
from ..items import QuoteItem
from scrapy.http import FormRequest
from scrapy_playwright.page import PageMethod

class QuotesspiderSpider(scrapy.Spider):
    name = "quotesspider"

    def start_requests(self):
        url = "https://quotes.toscrape.com/scroll"
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_methods=[
                PageMethod('wait_for_selector', 'div.quote'),
                PageMethod('evaluate', 'window.scrollBy(0, document.body.scrollHeight)'),
                PageMethod('wait_for_selector', 'div.quote:nth-child(11)'),
            ],
            errback=self.errback 
        ))


    
    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()
        # -------------------------FOR SCRAPING------------------------
        for quote in response.css('div.quote'):
            quote_item = QuoteItem()
            quote_item['text'] = quote.css("span.text::text").get()
            quote_item['author'] = quote.css("small.author::text").get()
            quote_item['tags']= quote.css("a.tag::text").get()
            yield quote_item

        # next_page= response.css('.next a').xpath('@href').get()
        # if next_page is not None:
        #     next_page_url = "https://quotes.toscrape.com" + next_page
        #     yield scrapy.Request(url=next_page_url, meta =dict(
        #     playwright = True,
        #     playwright_include_page = True,
        #     playwright_page_methods = [
        #         PageMethod('wait_for_selector', 'div.quote')
        #     ],
        #     errback = self.errback 
        # ))

        # ----------------------------FOR LOGIN--------------------------------
        # token = response.css('input[name="csrf_token"]').xpath('@value').get()
        # if not token:
        #     self.logger.error("CSRF token not found!")
        #     return

        # self.logger.info("Attempting to log in...")
        
        # return FormRequest.from_response(response, formdata={
        #     'csrf_token': token,
        #     'username': "jpt@jpt.com",
        #     'password': "123456789"
        # }, callback=self.start_scraping)


    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

    def start_scraping(self,response):
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