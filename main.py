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
# rewrite using scrapy library


def get_driver():
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)
    driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def browser_function():

    driver = get_driver()
    website = MainPage(driver=driver)

    # topics important for business use
    topics = ["Podatek od towarów i usług!", "Podatek dochodowy od osób prawnych!"]

    tic = time.perf_counter()
    website.get_pages_data_in_range(1, 101, 1, topic=topics[1])
    # website.get_all_data(topic=topics[1])

    tac = time.perf_counter()
    print(tac-tic)

    website.export_data_to_csv(topics[1] + ".csv")
    driver.quit()


if __name__ == "__main__":
    browser_function()
