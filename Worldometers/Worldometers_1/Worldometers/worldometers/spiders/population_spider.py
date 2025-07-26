import scrapy

class PopulationSpider(scrapy.Spider):
    name = "population"
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        # Extraction des lignes de la table
        rows = response.xpath('//table[contains(@class, "table")]/tbody/tr')
        for row in rows:
            yield {
                'country': row.xpath('./td[2]/a/text()').get(),
                'population': row.xpath('./td[3]/text()').get(),
                'yearly_change': row.xpath('./td[4]/text()').get(),
                'net_change': row.xpath('./td[5]/text()').get(),
                'density': row.xpath('./td[6]/text()').get(),
                'land_area': row.xpath('./td[7]/text()').get(),
                'migrants': row.xpath('./td[8]/text()').get(),
                'fert_rate': row.xpath('./td[9]/text()').get(),
                'med_age': row.xpath('./td[10]/text()').get(),
                'urban_pop': row.xpath('./td[11]/text()').get(),
                'world_share': row.xpath('./td[12]/text()').get(),
            }
