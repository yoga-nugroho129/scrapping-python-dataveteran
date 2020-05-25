# -*- coding: utf-8 -*-
import scrapy


class VetspiderSpider(scrapy.Spider):
    name = 'vetspider'
    start_urls = ['http://www.findalocalvet.com/Find-a-Veterinarian.aspx']

    def parse(self, response):
        cities_link = response.css("#SideByCity .itemresult a::attr(href)").getall()
        for city in cities_link:
            city_link = response.urljoin(city)
            yield scrapy.Request(city_link, callback=self.parse_city)
    
    # parse data inside city link
    def parse_city(self, response):
        clinics_link = response.css(".org::attr(href)").getall()
        for clinic_link in clinics_link:
            clinic = response.urljoin(clinic_link)
            yield scrapy.Request(clinic, callback=self.parse_clinic)

        # loop for next page
        next_page = response.css(".dataheader:contains('Next')::attr(href)").get()
        if next_page is not None:
            next_link = response.urljoin(next_page)
            yield scrapy.Request(next_link, callback=self.parse_city)

    def parse_clinic(self, response):
        yield {
            "Name" : response.css(".Results-Header h1::text").get(),
            "City" : response.css(".locality::text").get(),
            "State" : response.css(".region::text").get(),
            "Phone" : response.css(".Phone::text").get(),
            "Url" : response.url
        }