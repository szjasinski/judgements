import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor



class JacSpider(CrawlSpider):
    name = "jac"
    allowed_domains = ["orzeczenia.nsa.gov.pl"]
    start_urls = ["https://orzeczenia.nsa.gov.pl/cbo/find?p=1"]

    def parse(self, response):
        # title = response.xpath('//*[@class="info-list-value"]')
        links_list = response.xpath("//a[contains(text(),'Wyrok')]/@href").getall()
        return {"links": links_list}
