from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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

    # on results page
    links = main_page.links_list
    loop = range(len(links))

    for i in loop:
        links[i].click()
        judgement_data = main_page.details_dict
        database.append(judgement_data)
        driver.back()
        links = main_page.links_list

    print(len(database))
    for x in database:
        print(x["nazwa"], x['Data orzeczenia'], x['Sędziowie'])

    # driver.quit()


if __name__ == "__main__":
    browser_function()
