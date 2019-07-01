import scrapy
from bs4 import BeautifulSoup
import sys

class QuotesSpider(scrapy.Spider):
    name = 'indeed-jobs'
    start_urls = [
        'https://www.indeed.co.in/jobs?q=software+developer&l=Malad%2C+Mumbai%2C+Maharashtra',
    ]

    def parse(self, response):
        for quote in response.css('div.jobsearch-SerpJobCard'):
            yield {
                'orgname': BeautifulSoup(quote.css('span.company::text').get(),'lxml').text ,
                'location': quote.css('div.location::text').get() ,
            }

        next_page = response.css('div.pagination a:last-child::attr("href")').get()
        print(next_page)
        if next_page is not None:
            yield response.follow(next_page, self.parse)