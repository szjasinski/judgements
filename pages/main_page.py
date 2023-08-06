from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from .base_element import BaseElement
from .base_page import BasePage


class MainPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://orzeczenia.nsa.gov.pl/cbo/query"
        self.database = {
                "nazwa": [],
                "SENTENCJA": [],
                "UZASADNIENIE": [],
                "Data orzeczenia": [],
                "Data wpływu": [],
                "Sąd": [],
                "Sędziowie": [],
                "Symbol z opisem": [],
                "Hasła tematyczne": [],
                "Skarżony organ": [],
                "Treść wyniku": [],
                "Powołane przepisy": [],
                "Sygn. powiązane": [],
                "Publikacja w u.z.o.": [],
                "Info.o glosach": [],
            }

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
    def current_page_num(self):
        locator = (By.CLASS_NAME, "top-linki")
        txt = BaseElement(self.driver, by=locator[0], value=locator[1]).text
        current_page = int(txt.split("Str. ")[1].split(" z ")[0])
        return current_page

    @property
    def max_page_num(self):
        locator = (By.CLASS_NAME, "top-linki")
        txt = BaseElement(self.driver, by=locator[0], value=locator[1]).text
        max_page = int(txt.split("Str. ")[1].split(" z ")[1].split(" Powrót do szukania")[0])
        return max_page

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
    # on ruling details page
    # ------------------
    @property
    def _nazwa(self):
        locator = (By.CLASS_NAME, "war_header")
        return BaseElement(self.driver, by=locator[0], value=locator[1]).text

    @property
    def ruling_data_dict(self):

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

    def append_ruling_data(self, ruling_data):
        db = self.database

        for key, value in ruling_data.items():
            db[key].append(value)

        m = max([len(value) for key, value in db.items()])
        for feature in db.keys():
            if len(db[feature]) < m:
                db[feature].append("-")

    def get_first_page_data(self):
        links = self.links_list
        for i in range(len(links)):
            links[i].click()
            self.append_ruling_data(self.ruling_data_dict)
            self.driver.back()
            links = self.links_list

    def get_page_data(self, url):
        # for pages with numbers greater than 1
        self.set_url(url)
        self.go()

        links = self.links_list
        for i in range(len(links)):
            links[i].click()
            self.append_ruling_data(self.ruling_data_dict)
            self.driver.back()
            links = self.links_list

    def print_log(self):
        db = self.database
        items_num = len(db['nazwa'])
        unique_items_num = len(set([db['nazwa'][i] for i in range(len(db['nazwa']))]))

        print("page ", self.current_page_num, " out of ", self.max_page_num)
        print("items: ", items_num, ". Unique items: ", unique_items_num)


    def get_n_pages_data(self, n):
        result_pages_num = n
        for n in range(result_pages_num):
            if n == 0:
                self.get_first_page_data()
            if n > 0:
                self.url = "https://orzeczenia.nsa.gov.pl/cbo/find?p=" + str(n + 2)
                self.get_page_data(self.url)

            self.print_log()


    def get_all_data(self):
        pass

