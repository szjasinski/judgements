from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from .base_element import BaseElement
from .base_page import BasePage


class MainPage(BasePage):

    url = "https://orzeczenia.nsa.gov.pl/cbo/query"

    # ------------------
    # on search page
    # ------------------
    @property
    def hasla_tematyczne_input(self):
        locator = (By.ID, "hasla")
        return BaseElement(self.driver, by=locator[0], value=locator[1])

    @property
    def szukaj_button(self):
        locator = (By.XPATH, "//input[@type='submit']")
        return BaseElement(self.driver, by=locator[0], value=locator[1])

    # ------------------
    # on results page
    # ------------------
    @property
    def links_list(self):
        decyzje_lub_opis = self.driver.find_elements(By.CLASS_NAME, "info-list-value")
        decyzje = [decyzje_lub_opis[i] for i in range(0, len(decyzje_lub_opis), 2)]
        # decyzja to wyrok lub postanowienie, interesuja nas jedynie wyroki
        linki = []
        for i in range(len(decyzje)):
            try:
                link = decyzje[i].find_element(By.PARTIAL_LINK_TEXT, 'Wyrok')
                linki.append(link)
            except NoSuchElementException:
                print("postanowienie - nie uwzgledniamy")
        return linki

    @property
    def nastepna_strona_button(self):
        locator = (By.CLASS_NAME,"nextpage")
        return BaseElement(self.driver, by=locator[0], value=locator[1])

    # ------------------
    # on details page
    # ------------------
    @property
    def _nazwa(self):
        locator = (By.CLASS_NAME, "war_header")
        return BaseElement(self.driver, by=locator[0], value=locator[1]).text

    @property
    def details_dict(self):

        driver = self.driver

        details_d = {"nazwa": self._nazwa}

        keys = driver.find_elements(By.CLASS_NAME, "lista-label")
        keys = [i.text for i in keys]

        values = driver.find_elements(By.CLASS_NAME, "info-list-value")
        values = [i.text for i in values]

        reszta = driver.find_elements(By.CLASS_NAME, "info-list-value-uzasadnienie")

        sentencja_value = reszta[0].text
        details_d['SENTENCJA'] = sentencja_value

        if 'UZASADNIENIE' in keys:
            uzasadnienie_value = reszta[1].text
            details_d['UZASADNIENIE'] = uzasadnienie_value

        for key, value in zip(keys, values):
            details_d[key] = value

        return details_d
