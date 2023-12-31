from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
import pandas as pd
import threading

from pages.main_page import MainPage

# TO DO:
# threading
# better locators
# export to sql in batches
# code organization in main.py
# exceptions handling - custom exceptions?
# processing
# track number of rulings
# ruling data dict in dictionary format convertable to pandas df
# correct language of variables (English/Polish inconsistent)
# more elegant functions in main_page.py


def get_driver():
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)
    driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def browser_function():

    driver = get_driver()
    main_page = MainPage(driver=driver)

    # tic = time.perf_counter()
    # main_page.get_nth_page_data(2)
    main_page.get_pages_data_in_range(1, 5, 2)
    main_page.get_pages_data_in_range(2, 5, 2)

    # tac = time.perf_counter()
    # print(tac-tic)

    main_page.export_data_to_csv("csv_file.csv")
    main_page.export_data_to_xlsx("excel_file.xlsx")

    driver.quit()


if __name__ == "__main__":
    browser_function()
