from typing import Iterable
import scrapy
from ..items import QuoteItem
from scrapy_playwright.page import PageMethod

class QuotesspiderSpider(scrapy.Spider):
    name = "quotesspider"

    def start_requests(self):
        url = "https://quotes.toscrape.com/"
        yield scrapy.Request(url, meta =dict(
            playwright = True,
            playwright_include_page = True,
            playwright_page_methods = [
                PageMethod('wait_for_selector', 'div.quote')
            ],
            errback = self.errback 
        ))

    
    def parse(self, response):

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

    async def errback(self, failure):
        page = failure.request.meta["playwrite_page"]
        await page.close()