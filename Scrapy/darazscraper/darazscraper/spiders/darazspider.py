import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import WebDriverWait



class ClientSideSpider(scrapy.Spider):
    name = 'darazspider'
    allowed_domains = ['https://www.daraz.com.np']  

    # Entry point for starting requests
    def start_requests(self):
        url = 'https://pages.daraz.com.np/wow/gcp/route/daraz/np/upr/router?hybrid=1&data_prefetch=true&prefetch_replace=1&at_iframe=1&wh_pid=%2Flazada%2Fchannel%2Fnp%2Fflashsale%2FeBQX2YfTXs&hide_h5_title=true&lzd_navbar_hidden=true&disable_pull_refresh=true&skuIds=105485983%2C128126693%2C129619760%2C128294831%2C157857545%2C122148470%2C129575275&spm=a2a0e.tm80335409.FlashSale.d_shopMore'
        yield SeleniumRequest(
            url=url, 
            callback=self.parse, 
            wait_time=1,
            script="""
            document.querySelector('a.button.J_LoadMoreButton').click();
            """,

        )



    def parse(self, response):
        driver = response.meta['driver']

        try:
            # Waiting for some element that appears after loading more items
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.sale-title'))
            )
        except Exception as e:
            self.logger.error(f"Error while waiting for content to load: {e}")

        # Give some additional wait time to ensure content is fully loaded
        time.sleep(5)

        # Now fetch the updated page source after clicking the button
        html = driver.page_source
        response = scrapy.Selector(text=html)

        title = response.css('.sale-title::text').getall()
        print("*******************************************")
        print(len(title))

        # Logging and yielding the scraped data
        self.logger.info(f'Total items after clicking Load More: {len(title)}')
        yield {
            'name': title
        }
        

    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()







