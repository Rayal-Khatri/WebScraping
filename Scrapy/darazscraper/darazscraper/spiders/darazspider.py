import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.utils.response import open_in_browser

class ClientSideSpider(scrapy.Spider):
    name = 'darazspider'
    allowed_domains = ['https://www.daraz.com.np']  # Replace with your target URL

    # Entry point for starting requests
    def start_requests(self):
        url = "https://www.daraz.com.np/catalog/?spm=a2a0e.tm80331706.search.d_go&q=keyboard%20fantech"
        yield scrapy.Request (url,
                meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[   
                        # -------------For SCROLLING --------------
                    # PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),  # Scroll to the bottom
                    PageMethod("wait_for_timeout", 2000),
                    # PageMethod("wait_for_load_state", "networkidle"),
                    # PageMethod('wait_for_selector', 'div.item-button'),
                    # PageMethod('stop')
                    # PageMethod("click", "a.J_LoadMoreButton"),
                    # # PageMethod("click", ".shopMoreBtn"),  # Click the button
                    # PageMethod("wait_for_timeout", 5000),
                    # PageMethod("wait_for_navigation")
                    ],
                errback=self.errback 
            )
        )

    def parse(self, response):
        open_in_browser(response)
        products = response.css('.flash-unit')
        
        # Iterate through each product container
        for product in products:
            name = product.css('.sale-title::text').get().strip()  # Get and clean the product name
            price = product.css('.sale-price::text').get().strip()  # Get and clean the product price
            url = product.css('.flash-unit-a').xpath('@href').get()
            
            # Yield the results
            yield {
                'name': name,
                'price': price,
                'url' : url
            }

    #     }
    # Error handling for Playwright
    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()
