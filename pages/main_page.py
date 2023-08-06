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

    def get_data(self):
        result_pages_num = 6
        for n in range(result_pages_num):

            if n > 0:
                new_url = "https://orzeczenia.nsa.gov.pl/cbo/find?p=" + str(n+2)
                self.set_url(new_url)
                self.go()

            # on results page
            links = self.links_list

            for i in range(len(links)):
                links[i].click()
                judgement_data = self.details_dict
                self.database.append(judgement_data)
                self.driver.back()
                links = self.links_list

            print("len database: ", str(len(self.database)))
            for x in self.database:
                print("Strona: ", str(n), ". Wyrok: ", x["nazwa"])

            print('udalo sie!')
            print("items: ", len(self.database))
            print("unique items: ", len(set([self.database[i]['nazwa'] for i in range(len(self.database))])))
