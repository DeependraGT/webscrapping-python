import scrapy
from selenium import webdriver
import time
import requests

class ProductSpider(scrapy.Spider):
    name = "product_spider"
    allowed_domains = ['iimjobs.com']
    start_urls = ['https://recruit.iimjobs.com/login']
    email = 'andleeb.qamar@greatdevelopers.com'
    password = '12345678'
    filePath = 'E:/DataScrapping/Resumes/'

    def __init__(self):
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

                # Checking Login request success or not
                """self.driver.get("https://recruit.iimjobs.com/")
                loggedinName = self.driver.find_element_by_class_name('heading')"""
               

                # Loading the new application resumes
                self.driver.get('https://recruit.iimjobs.com/job/715710/applications')
                time.sleep(15)
                resumes = self.driver.find_elements_by_class_name('candidateDownloadResume')

                # Download and saving resumes
                for ele in resumes:
                    resumehref = ele.get_attribute('data-href')
                    self.downloadResumes(resumehref)
            except:
                break
        
        self.driver.close()

    # Download and save resumes on specific folder
    def downloadResumes(self,resumeurl):
        urlSplits = resumeurl.split('/')
        arrayLength = len(urlSplits)
        generatedFileName = self.filePath + urlSplits[arrayLength - 2] + '_' + urlSplits[arrayLength-1]

        # Get the file from url and saved the file as generated name
        myfile = requests.get(resumeurl, allow_redirects=True)
        open(generatedFileName, 'wb').write(myfile.content)