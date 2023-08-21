import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from jac_scraper.items import JacScraperItem

urls_generator = ["https://orzeczenia.nsa.gov.pl/cbo/find?p=" + str(i) for i in range(1, 2)]


class JacSpider(CrawlSpider):
    name = "jac"
    allowed_domains = ["orzeczenia.nsa.gov.pl"]
    start_urls = urls_generator

    rules = (
        Rule(LinkExtractor(allow=(r"orzeczenia.nsa.gov.pl/doc/.*",),
                           restrict_xpaths=('//td[@class="info-list-value nk"]','//td[@class="info-list-value "]')),
             callback="parse_item"),
    )

    def parse_item(self, response):
        # self.logger.info("------- judgement details page: ----> %s ", response.url)

        item = JacScraperItem()
        nazwa = response.xpath('//span[@class="war_header"]/text()').get()
        url = response.url

        item["nazwa"] = nazwa
        item["url"] = url

        cechy_tabela = response.xpath('//td[@class="lista-label"]/text()').getall()
        print(cechy_tabela)
        # wartosci_tabela = response.xpath('//td[@class="info-list-value"]/table/tr/td/text()').getall()
        wartosci_tabela = response.xpath('//td[@class="info-list-value"]')

        data_orzeczenia = response.xpath('//td[@class="info-list-value"]/table/tr/td[1]/text()').get()
        prawomocnosc = response.xpath('//td[@class="info-list-value"]/table/tr/td[2]/text()').get()

        item["prawomocnosc"] = prawomocnosc

        print("data orzeczenia", data_orzeczenia)
        print("prawomocnosc", prawomocnosc)

        for i in range(len(wartosci_tabela)):
            ab = wartosci_tabela[i].xpath('.//text()').get()
            wartosci_tabela[i] = ab
        wartosci_tabela[0] = data_orzeczenia
        print(wartosci_tabela)


        cechy_tekst = response.xpath('//td[@class="info-list-label-uzasadnienie"]/div/text()').getall()

        # WRONG!!!!
        wartosci_tekst = response.xpath('//td[@class="info-list-label-uzasadnienie"]/span/p/text()').getall()

        # assert len(cechy_tekst) == len(wartosci_tekst)
        for cecha, wartosc in zip(cechy_tabela, wartosci_tabela):
            if cecha == "Data orzeczenia":
                item['data_orzeczenia'] = wartosc
            elif cecha == "Data wpływu":
                item['data_wplywu'] = wartosc
            elif cecha == "Sąd":
                item['sad'] = wartosc
            elif cecha == "Sędziowie":
                item['sedziowie'] = wartosc
            elif cecha == "Skarżony organ":
                item['skarzony_organ'] = wartosc
            elif cecha == "Symbol z opisem":
                item['symbol_z_opisem'] = wartosc
            elif cecha == "Hasła tematyczne":
                item['hasla_tematyczne'] = wartosc
            elif cecha == "Publikacja w u.z.o.":
                item['poblikacja_w_uzo'] = wartosc
            elif cecha == "Treść wyniku":
                item['tresc_wyniku'] = wartosc
            elif cecha == "Powołane przepisy":
                item['powolane_przepisy'] = wartosc
            elif cecha == "Sygn. powiązane":
                item['sygn_powiazane'] = wartosc
            else:
                with open("errors.txt", "a") as file_object:
                    file_object.write("cecha:", cecha, len(cecha))
                    file_object.write("url:", url)
                    file_object.write("\n")

        for cecha, wartosc in zip(cechy_tekst, wartosci_tekst):
            if cecha == "Sentencja":
                # item['sentencja'] = wartosc
                pass
            elif cecha == "Uzasadnienie":
                item['uzasadnienie'] = wartosc
            elif cecha == "Tezy":
                item['tezy'] = wartosc
            else:
                with open("errors.txt", "a") as file_object:
                    file_object.write(cecha)
                    file_object.write("\n")

        return item

#
#
# # CLASS FOR SCRAPING PRACUJ.PL JOB OFFERS
# pracuj_urls_generator = ["https://it.pracuj.pl/praca?pn=" + str(i) for i in range(1,2)]
#
#
# class JacSpider(CrawlSpider):
#
#     name = "pracuj"
#     allowed_domains = ["pracuj.pl"]
#     start_urls = pracuj_urls_generator
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
