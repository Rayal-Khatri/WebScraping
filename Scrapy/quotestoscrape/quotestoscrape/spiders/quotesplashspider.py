import scrapy
from ..items import QuoteItem

from scrapy_splash import SplashRequest 


lua_script = """
function main(splash,args)
    assert(splash:go(args.url))

    local element = splash:select('body > div > nav > ul > li > a')
    element:mouse_click()
    
    splash:wait(splash.args.wait)  
    return splash:html()
end
"""


class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        url = 'https://quotes.toscrape.com/js/'
        yield SplashRequest(
            url, 
            callback=self.parse, 
            endpoint='execute', 
            args={'wait': 2, 'lua_source': lua_script, url: 'https://quotes.toscrape.com/js/'}
            )

    def parse(self, response):
        for quote in response.css('div.quote'):
            quote_item = QuoteItem()
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
            yield quote_item