import scrapy
from selenium import webdriver
import time
import requests
import logging
import logging.handlers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOG_FILENAME = 'iimjobs-selenium.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

# Set up a specific logger with our desired output level
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME)

my_logger.addHandler(handler)

class ProductSpider(scrapy.Spider):
    name = "product_spider"
    allowed_domains = ['iimjobs.com']
    start_urls = ['https://recruit.iimjobs.com/login']
    email = 'andleeb.qamar@greatdevelopers.com'
    password = '12345678'
    filePath = 'E:/DataScrapping/Resumes/'

    def __init__(self):
        my_logger.debug("Initializing the spider")
        self.driver = webdriver.Chrome()

    def parse(self, response):
        self.driver.get(response.url)

        while True:
            email = self.driver.find_element_by_id('email')
            email.clear()
            email.send_keys(self.email)

            password = self.driver.find_element_by_id('password')
            password.clear()
            password.send_keys(self.password)

            login = self.driver.find_element_by_id('login')

            try:
                
                # Clicking on the submit button after filling email/ password
                login.click()
                time.sleep(15)

                #wait = WebDriverWait(self.driver, 10)
                #element = wait.until(EC.element_to_be_clickable((By.ID, 'chat-div')))

                # Checking Login request success or not
                """self.driver.get("https://recruit.iimjobs.com/")
                loggedinName = self.driver.find_element_by_class_name('heading')"""
               

                self.driver.get('https://recruit.iimjobs.com/jobs')
                time.sleep(15)
                jobs = self.driver.find_elements_by_css_selector('.jobEngagement a.jobApplicationsLink')

                if jobs is None:
                    break

                for job in jobs:
                    applicationUrl = job.get_attribute('href')
                    my_logger.debug("Job Urls : " + applicationUrl)

                    if applicationUrl is None:
                        break

                    self.driver.get(applicationUrl)
                    time.sleep(15)
                    profiles = self.driver.find_elements_by_css_selector('.candidateRow a.openCandidateLink')

                    if profiles is None:
                        break

                    maxprofileCounter = 10
                    for profile in profiles:
                        if maxprofileCounter == 0:
                            break

                        profileUrl = profile.get_attribute('href')
                        maxprofileCounter -= 1
                        my_logger.debug("Profile Url {}: {}".format(maxprofileCounter,profileUrl))

                        self.driver.get(profileUrl)
                        time.sleep(15)
                        element =  self.driver.find_element_by_css_selector('div.email-address')
                        my_logger.debug(element)
                        my_logger.debug(element.text)   



                # Loading the new application resumes
                  """  self.driver.get(applicationUrl)
                    time.sleep(15)
                    resumes = self.driver.find_elements_by_class_name('candidateDownloadResume')"""

                    # Download and saving resumes
                   """ for ele in resumes:
                        resumehref = ele.get_attribute('data-href')
                        self.downloadResumes(resumehref)"""


            except:
                break
        
        self.driver.close()




    # Download and save resumes on specific folder
    def downloadResumes(self,resumeurl):
        urlSplits = resumeurl.split('/')
        arrayLength = len(urlSplits)
        generatedFileName = self.filePath + urlSplits[arrayLength - 2] + '_' + urlSplits[arrayLength-1]
        self.log("Generated File Name : %s" % generatedFileName)
        my_logger.debug("Generated File Name : %s" % generatedFileName)

        # Get the file from url and saved the file as generated name
        myfile = requests.get(resumeurl, allow_redirects=True)
        open(generatedFileName, 'wb').write(myfile.content)
