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
import pika
import json

LOG_FILENAME = 'naukri.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

# Set up a specific logger with our desired output level
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME)

formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s : %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

handler.setFormatter(formatter)

my_logger.addHandler(handler)

class NaukriSpider(scrapy.Spider):
    name = "Naukri"
    allowed_domains = ['naukri.com']
    start_urls = ['https://www.naukri.com/']
    email = 'andleeb.qamar@greatdevelopers.com'
    password = 'Aq@12345'
    filePath = 'E:/DataScrapping/Resumes/'
    connection = None
    channel = None

    def __init__(self):
        my_logger.debug("Initializing the spider")
        options = webdriver.ChromeOptions()
        chromedriver = "chromedriver.exe"
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")       # ("--kiosk") for MAC
        options.add_argument("--disable-popups")
        self.driver = webdriver.Chrome(chrome_options=options,executable_path=chromedriver)


    def ConnectRabbitmq(self):
        my_logger.debug("Connecting with rabbitmq")
        credentials = pika.PlainCredentials('deependra', 'deependra')
        connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.6.51',5672,'/',credentials))
        channel = connection.channel()
        my_logger.debug("Connected with rabbitmq")
        return connection, channel

    def GetMessagefromQueue(self):
        if self.connection is None:
          self.connection, self.channel = self.ConnectRabbitmq()
        
        if self.connection.is_open:
            my_logger.debug("Reading the message from rabbitmq")
            method, header, body = self.channel.basic_get(queue="HBNaukriQueue")
            p = json.loads(body)
            
        return method, header , p
        #channel.basic_ack(delivery_tag=method.delivery_tag)

    def parse(self, response):
        self.driver.get("https://www.naukri.com/recruit/login")
        self.driver.maximize_window()
        time.sleep(10)
        
        tabElement = self.driver.find_element_by_xpath('//*[@id="toggleForm"]/li[2]')
        tabElement.click()
        time.sleep(10)

        method, header, body = self.GetMessagefromQueue()
        my_logger.debug("Fetched the body")
        time.sleep(10)
        script = "$('#loginEmail').val('"+body["email"]+"');$('#password').val('"+body["password"]+"');"
        
        self.channel.basic_ack(delivery_tag=method.delivery_tag)
        
        print script
        self.driver.execute_script(script)
        time.sleep(15)
        login = self.driver.find_element_by_xpath('//*[@id="loginBtn"]')
        login.click()
        time.sleep(45)
        
        method, header, body = self.GetMessagefromQueue()
        otpEle = self.driver.find_element_by_id('otpCode')
        otpEle.clear()
        otpEle.send_keys(body["OTP"])
        self.channel.basic_ack(delivery_tag=method.delivery_tag)

        try:
                
            # Clicking on the submit button after filling email/ password
            verifyEle = self.driver.find_element_by_id('verifyOtpBtn')
            verifyEle.click()
            time.sleep(15)

            # Close Rabbitmq Connection
            self.connection.close()

            naukriCookies = self.driver.get_cookies()
            my_logger.debug(naukriCookies)
            
            time.sleep(60)

            self.driver.get("https://rms.naukri.com/profile/inbox")
            time.sleep(10)

            self.driver.get('https://rms.naukri.com/application/viewApplication/6865598?_REF=I')
            time.sleep(10)

            name = self.driver.find_element_by_xpath('//*[@id="viewBasicDiv"]/div[1]/div[1]/div[1]/div[1]').text
            email = self.driver.find_element_by_xpath('//*[@id="candCont"]/div[1]/div/a').text
            phone =  self.driver.find_element_by_id('candidatePhoneId').text
            picUrl = self.driver.find_element_by_xpath('//*[@id="logo"]').get_attribute('src')
            resumeUrl = self.driver.find_element_by_xpath('//*[@id="atachedDocSection"]/div/ul/div/li/a[1]').get_attribute('href')

            profile = {'name':name,'email':email,'mobile':phone,'picurl':picUrl,'resumeurl':resumeUrl}
            my_logger.debug(profile)

        except:
            my_logger.debug("Getting error")


    

        

        