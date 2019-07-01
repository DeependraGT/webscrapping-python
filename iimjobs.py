import scrapy
from scrapy.http import FormRequest
from login_form import fill_login_form


class LoginSpider(scrapy.Spider):
    start_urls = ["https://recruit.iimjobs.com/login"]
    email = "andleeb.qamar@greatdevelopers.com"
    password = "12345678"
    
    def parse(self, response):
        print(response)
        args, url, method = fill_login_form(response.url, response.body, self.email, self.password)
        return FormRequest(url, method=method, formdata=args, callback=self.after_login)
    def after_login(self, response):
        print(response)