import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from scrapy.selector import Selector 
import logging
import time

class DarazItemSpider(scrapy.Spider):
    name = "daraz_item"
    allowed_domains = ['https://www.daraz.com.np','www.daraz.com.np','daraz.com.np']  

    def start_requests(self):
        url = "https://www.daraz.com.np/catalog/?spm=a2a0e.tm80335409.search.2.28a379e0oo0co0&q="  
        keyword = input("*****************Enter The search Keywoard****************")    
        url = url + keyword.replace(' ', '%20')
        # url = "https://www.daraz.com.np/catalog/?page=3&q=chana"  # this code is for testing and is the end of the search result
        yield SeleniumRequest(
            url=url, 
            callback=self.parse,  
        )

    def parse(self, response):
        items = []
        driver = response.meta['driver'] 
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 1.2);")  # Wait for new content to load

        # Initial pagination button setup
        while True:
            # Get and parse page source
            current_html = driver.page_source
            current_page_selector = Selector(text=current_html)
            items.extend(current_page_selector.css('.Bm3ON'))  # Add items from current page
            
            # print(f"***************************************{len(items)}")
            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ant-pagination-item-link")))
            # Check if next button is available and not disabled
            pagination_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.ant-pagination-next[aria-disabled="false"] button')))
            
            disabled = not driver.execute_script("return arguments[0].hasAttribute('disabled')", button)
            if disabled:
                break

            # Click the button and wait for page update
            current_url = driver.current_url
            pagination_button.click()
            WebDriverWait(driver, 10).until(EC.url_changes(current_url))
            
            # Scroll after navigation to load new items
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 1.2);")
            time.sleep(1)  # Adjust if necessary to let content load fully
        print(f"***************************************{len(items)}")
        pass



