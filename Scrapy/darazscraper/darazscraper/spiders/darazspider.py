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
        )



    def parse(self, response):

        # -------------------------------TO LOAD MORE--------------------
        driver = response.meta['driver']

        while True:
            try:
                # Wait for the "Load More" button to be clickable
                load_more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.button.J_LoadMoreButton'))
                )
                load_more_button.click()  # Click the "Load More" button
                time.sleep(3)  # Wait for new content to load

            except Exception as e:
                # Break the loop if the button is not found or not clickable
                print("No more 'Load More' button found or unable to click:", e)
                break

        # # Now fetch the updated page source after clicking the button
        html = driver.page_source
        response = scrapy.Selector(text=html)

        title = response.css('.sale-title::text').getall()
        print("*******************************************")
        print(len(title))

        # Logging and yielding the scraped data
        # self.logger.info(f'Total items after clicking Load More: {len(title)}')
        yield {
            'name': title
        }
        

    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()







