from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

from pages.main_page import MainPage


def browser_function():
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)
    driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # database is a list of dictionaries, each containing data of a single judgement
    database = []

    # on search page
    main_page = MainPage(driver=driver)
    main_page.go()
    main_page.hasla_tematyczne_input.input_text("Podatek od czynności cywilnoprawnych!")
    main_page.szukaj_button.click()

    # tic = time.perf_counter()

    result_pages_num = 6
    for n in range(result_pages_num):

        if n > 0:
            new_url = "https://orzeczenia.nsa.gov.pl/cbo/find?p=" + str(n+2)
            main_page.set_url(new_url)
            main_page.go()

        # on results page
        links = main_page.links_list
        loop = range(len(links))

        for i in loop:
            links[i].click()
            judgement_data = main_page.details_dict
            database.append(judgement_data)
            driver.back()
            links = main_page.links_list

        print("len database: ", str(len(database)))
        for x in database:
            print("Strona: ", str(n), ". Wyrok: ", x["nazwa"])



        # object for number of pages

        # tac = time.perf_counter()
        # print(tac-tic)

    print('udalo sie!')
    print(len(database))
    print(len(set([database[i]['nazwa'] for i in range(len(database))])))

    data = {}
    for d in database:
        for key, value in d.items():
            data[key] = []

    for i in range(len(database)):
        for key, value in database[i].items():
            data[key].append(value)

        m = max([len(value) for key, value in data.items()])
        for key in data.keys():
            if len(data[key]) < m:
                data[key].append("-")

    for i in range(len(data['UZASADNIENIE'])):
        data['UZASADNIENIE'][i] = 'szczegoly'

    df = pd.DataFrame(data)
    # df.to_excel('data.xlsx')
    df.to_excel("file.xlsx", engine='xlsxwriter')

    df.to_csv('file.csv')

    driver.quit()


if __name__ == "__main__":
    browser_function()
