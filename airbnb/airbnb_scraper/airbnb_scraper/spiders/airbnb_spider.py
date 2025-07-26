import scrapy

class AirbnbSpider(scrapy.Spider):
    # Le nom du spider doit être 'airbnb' ou un autre nom unique
    name = 'airbnb'  # Cela définit le nom du spider

    allowed_domains = ['airbnb.com']
    start_urls = [
        'https://www.airbnb.com/s/Paris/homes?checkin=2023-12-20&checkout=2023-12-23'
    ]

    def parse(self, response):
        listings = response.css('a[data-check-info-section="true"]::attr(href)').getall()
        for listing in listings:
            listing_url = response.urljoin(listing)
            yield scrapy.Request(url=listing_url, callback=self.parse_listing)

        next_page = response.css('a[aria-label="Next"]::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

    def parse_listing(self, response):
        yield {
            'title': response.css('h1[data-testid="title"]::text').get(),
            'price': response.css('span[data-testid="price"]::text').get(),
            'rooms': response.css('span[data-testid="rooms"]::text').get(),
            'reviews': response.css('span[data-testid="reviews-count"]::text').get(),
            'rating': response.css('span[data-testid="rating"]::text').get(),
            'amenities': response.css('div[data-testid="amenities"]::text').getall(),
        }
