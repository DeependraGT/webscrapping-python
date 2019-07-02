import scrapy
from scrapy.http import FormRequest
from login_form import fill_login_form


class LoginSpider(scrapy.Spider):
    name = "LoginSpider"
    start_urls = ["https://recruit.iimjobs.com/login"]
    email = "andleeb.qamar@greatdevelopers.com"
    password = "12345678"
    
    def parse(self, response):        
        #return FormRequest.from_response(response, formdata={'email':'andleeb.qamar@greatdevelopers.com','password':'123456'}, callback=self.after_login)
        print('response body')
        print(response.body)
        args, url, method = fill_login_form(response.url, response.body, self.email, self.password)
        return FormRequest(url, method=method, formdata=args, callback=self.after_login)

    def after_login(self, response):
        print("response")
        print(response)