import scrapy
from selenium import webdriver
import time

class ProductSpider(scrapy.Spider):
    name = "product_spider"
    allowed_domains = ['iimjobs.com']
    start_urls = ['https://recruit.iimjobs.com/login']

    def __init__(self):
        self.driver = webdriver.Chrome()

    def parse(self, response):
        self.driver.get(response.url)

        while True:
            email = self.driver.find_element_by_id('email')
            email.clear()
            email.send_keys('andleeb.qamar@greatdevelopers.com')

            password = self.driver.find_element_by_id('password')
            password.clear()
            password.send_keys('12345678')

            login = self.driver.find_element_by_id('login')

            try:
                login.click()

                # get the data and write it to scrapy items
            except:
                break
        time.sleep(30)
        self.driver.close()