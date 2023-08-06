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

    # on search page
    main_page = MainPage(driver=driver)
    main_page.go()
    main_page.hasla_tematyczne_input.input_text("Podatek od czynności cywilnoprawnych!")
    main_page.szukaj_button.click()

    # tic = time.perf_counter()
    main_page.get_n_pages_data(5)
    # object for number of pages

    # tac = time.perf_counter()
    # print(tac-tic)

    data = main_page.database
    df = pd.DataFrame(data)
    # df.to_excel('data.xlsx')
    df.to_excel("file.xlsx", engine='xlsxwriter')

    df.to_csv('file.csv')

    driver.quit()


if __name__ == "__main__":
    browser_function()
