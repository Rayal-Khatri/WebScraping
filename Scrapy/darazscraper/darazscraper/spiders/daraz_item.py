import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import logging
import time

class DarazItemSpider(scrapy.Spider):
    name = "daraz_item"
    allowed_domains = ['https://www.daraz.com.np','www.daraz.com.np','daraz.com.np']  

    def start_requests(self):
        url = "https://www.daraz.com.np/catalog/?spm=a2a0e.tm80335409.search.2.28a379e0oo0co0&q="  
        keyword = input("*****************Enter The search Keywoard****************")    
        url = url + keyword.replace(' ', '%20')
        yield SeleniumRequest(
            url=url, 
            callback=self.parse,  
            wait_time=1   
        )

    def parse(self, response):
        driver = response.meta['driver'] 
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 1.2);")  # Wait for new content to load
        time.sleep(1)
        for item in response.css('.Bm3ON'):
            url = item.css('a').xpath('@href').get()
            yield SeleniumRequest(
            url="https:"+url,
            callback=self.parse_item_page,
        )
          
    def parse_item_page(self, response):
        driver = response.meta['driver']
        print("*******************************************")

        # Scroll to the middle of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")  # Scroll to the middle
        time.sleep(3)
        try:
            rating = driver.find_element(By.CSS_SELECTOR, 'span.score-average').text.strip()
        except Exception as e:
            rating = 'No rating' 

        yield {
            'name': response.css('.pdp-mod-product-badge-title::text').get(),
            'price': response.css('.pdp-price_size_xl::text').get(),
            'delivery_price': response.css('.delivery-option-item_type_standard .no-subtitle::text').get(),
            'rating':rating,
            'seller': response.css('.seller-name__detail-name::text').get(),
            'seller_rating': response.css('.rating-positive::text').get(),
            'delivery_rating' : response.css('.info-content:nth-child(2) .seller-info-value::text').get(),
            'stock': response.css('#module_quantity-input input').xpath('@max').get()
        }

