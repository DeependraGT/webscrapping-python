import scrapy
from bs4 import BeautifulSoup
import sys
import re

class IndeedSpider(scrapy.Spider):
    name = 'indeed'
    start_urls = [
        'https://www.indeed.co.in/jobs?q=software+developer&l=Malad%2C+Mumbai%2C+Maharashtra',
    ]

    def parse(self, response):
        for quote in response.css('div.jobsearch-SerpJobCard'):
            yield {
                'jobtitle':self.removehtml_tags(quote.css('a.jobtitle').get()),
                'orgname': self.removehtml_tags(quote.css('span.company').get())  ,
                'location': self.removehtml_tags(quote.css('div.location').get()) ,
            }

        next_page = response.css('div.pagination a:last-child::attr("href")').get()
        print(next_page)
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def removehtml_tags(self,text):
        try:
            clean = re.compile('<.*?>')
            return re.sub(clean, '', text) 
        except:
            return ""