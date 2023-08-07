from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import time
import multiprocessing

from pages.main_page import MainPage


def browser_function():

    def func(n, results):
        def get_driver():
            options = ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_experimental_option("detach", True)
            driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)
            return driver

        driver = get_driver()
        website = MainPage(driver=driver)
        time.sleep(n * 10)
        website.get_pages_data_in_range(start=n + 1, stop=6, step=threads_num)
        results[n] = website.database

    results = {}
    threads_num = 2

    processes = [multiprocessing.Process(target=func, args=(n, results)) for n in range(threads_num)]
    [t.start() for t in processes]
    [t.join() for t in processes]

    print("successful threads:", len(results))


if __name__ == "__main__":
    browser_function()
