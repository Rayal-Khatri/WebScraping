import scrapy
from scrapy.utils.response import open_in_browser
from scrapy_playwright.page import PageMethod

class AmazonspiderSpider(scrapy.Spider):
    name = "amazonspider"
    allowed_domains = ["https://www.daraz.com.np"]

    def start_requests(self):
        url = "https://pages.daraz.com.np/wow/gcp/route/daraz/np/upr/router?hybrid=1&data_prefetch=true&prefetch_replace=1&at_iframe=1&wh_pid=%2Flazada%2Fchannel%2Fnp%2Fflashsale%2FeBQX2YfTXs&hide_h5_title=true&lzd_navbar_hidden=true&disable_pull_refresh=true&skuIds=105485983%2C128126693%2C129619760%2C128294831%2C157857545%2C122148470%2C129575275&spm=a2a0e.tm80335409.FlashSale.d_shopMore"
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
                    
                    PageMethod("click", "a.J_LoadMoreButton"),
                    # PageMethod("click", ".shopMoreBtn"),  # Click the button
                    # PageMethod("wait_for_navigation")
                    ],
                errback=self.errback 
            )
        )

    def parse(self, response):
        open_in_browser(response)
        yield {
            'name': response.css('.sale-title::text').getall()
        }


    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
