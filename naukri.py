import scrapy
from selenium import webdriver
import time
import requests
import logging
import logging.handlers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

LOG_FILENAME = 'naukri.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

# Set up a specific logger with our desired output level
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME)

my_logger.addHandler(handler)

class NaukriSpider(scrapy.Spider):
    name = "Naukri"
    allowed_domains = ['naukri.com']
    start_urls = ['https://www.naukri.com/recruit/login']
    email = 'andleeb.qamar@greatdevelopers.com'
    password = 'Aq@12345'
    filePath = 'E:/DataScrapping/Resumes/'
    

    def __init__(self):
        my_logger.debug("Initializing the spider")
        options = webdriver.ChromeOptions()
        chromedriver = "chromedriver.exe"
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")       # ("--kiosk") for MAC
        options.add_argument("--disable-popups")
        self.driver = webdriver.Chrome(chrome_options=options,executable_path=chromedriver)

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.maximize_window()
        time.sleep(30)
        email = self.driver.find_element_by_id('loginEmail')
        email.clear()
        email.send_keys(self.email)

        password = self.driver.find_element_by_id('password')
        password.clear()
        password.send_keys(self.password)

        login = self.driver.find_element_by_id('loginBtn')

        try:
                
                # Clicking on the submit button after filling email/ password
                login.click()
                time.sleep(15)

        except:
            my_logger.debug("Getting error")