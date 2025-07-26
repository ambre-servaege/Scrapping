import scrapy
import logging

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        logging.info("Parsing the main page")
        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath("./text()").get()
            link = country.xpath("./@href").get()
            logging.info(f"Found country: {name} with link: {link}")

            if name and link:
                yield response.follow(url=link, callback=self.parse_country, meta={'country_name': name})

    def parse_country(self, response):
        name = response.request.meta['country_name']
        logging.info(f"Parsing country page for: {name}")
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        for row in rows:
            year = row.xpath("./td[1]/text()").get()
            population = row.xpath("./td[2]/strong/text()").get()
            logging.info(f"Year: {year}, Population: {population}")

            if year and population:
                yield {
                    'country_name': name,
                    'year': year,
                    'population': population
                }