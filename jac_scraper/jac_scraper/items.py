# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JacScraperItem(scrapy.Item):

    nazwa = scrapy.Field()
    url = scrapy.Field()
    data_orzeczenia = scrapy.Field()
    prawomocnosc = scrapy.Field()
    sad = scrapy.Field()
    sedziowie = scrapy.Field()
    symbol_z_opisem = scrapy.Field()
    hasla_tematyczne = scrapy.Field()
    poblikacja_w_uzo = scrapy.Field()
    tresc_wyniku = scrapy.Field()
    sentencja = scrapy.Field()
    uzasadnienie = scrapy.Field()
    tezy = scrapy.Field()
    data_wplywu = scrapy.Field()
    skarzony_organ = scrapy.Field()
    powolane_przepisy = scrapy.Field()
    sygn_powiazane = scrapy.Field()


    # ITEMS FOR PRACUJ.PL SCRAPER
    # job_title = scrapy.Field()
    # employer = scrapy.Field()
    # price_from = scrapy.Field()
    # price_to = scrapy.Field()
    # price_unit = scrapy.Field()