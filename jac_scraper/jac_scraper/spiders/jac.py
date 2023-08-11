import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from jac_scraper.items import JacScraperItem


urls_generator = ["https://orzeczenia.nsa.gov.pl/cbo/find?p=" + str(i) for i in range(1,3)]

class JacSpider(CrawlSpider):
    name = "jac"
    allowed_domains = ["orzeczenia.nsa.gov.pl"]
    start_urls = urls_generator

    rules = (
        Rule(LinkExtractor(allow=(r"orzeczenia.nsa.gov.pl/doc/.*",)), callback="parse_item"),
    )

    def parse_item(self, response):
        self.logger.info("Hi, this is a judgement details page! %s", response.url)
        item = JacScraperItem()
        item["nazwa"] = response.xpath('//span[@class="war_header"]/text()').get()
        # item["employer"] = response.xpath('//h2[@data-scroll-id="employer-name"]/text()').get()
        # item["price_from"] = response.xpath('//span[@data-test="text-earningAmountValueFrom"]/text()').get()
        # item["price_to"] = response.xpath('//span[@data-test="text-earningAmountValueTo"]/text()').get()
        # item["price_unit"] = response.xpath('//span[@data-test="text-earningAmountUnit"]/text()').get()

        return item






# CLASS FOR SCRAPING PRACUJ.PL JOB OFFERS
# urls_generator = ["https://it.pracuj.pl/praca?pn=" + str(i) for i in range(1,3)]
#
#
# class JacSpider(CrawlSpider):
#
#     name = "pracuj"
#     allowed_domains = ["pracuj.pl"]
#     start_urls = urls_generator
#
#     rules = (
#         Rule(LinkExtractor(allow=(r"praca/.*,oferta,.*",)), callback="parse_item"),
#     )
#
#     def parse_item(self, response):
#         self.logger.info("Hi, this is a job offer page! %s", response.url)
#         item = JacScraperItem()
#         item["job_title"] = response.xpath('//h1[@data-scroll-id="job-title"]/text()').get()
#         item["employer"] = response.xpath('//h2[@data-scroll-id="employer-name"]/text()').get()
#         item["price_from"] = response.xpath('//span[@data-test="text-earningAmountValueFrom"]/text()').get()
#         item["price_to"] = response.xpath('//span[@data-test="text-earningAmountValueTo"]/text()').get()
#         item["price_unit"] = response.xpath('//span[@data-test="text-earningAmountUnit"]/text()').get()
#
#         return item
