from selenium import webdriver
import threading

from pages.main_page import MainPage


class Browser():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.website = MainPage(driver=self.driver)

    def fun(self, n, threads_num, results):
        self.website.get_pages_data_in_range(start=n + 1, stop=6, step=threads_num)
        results[n] = self.website.database

    def get_driver(self):
        return self.driver


def func(n, threads_num, results):
    browser = Browser
    try:
        browser.fun(n, threads_num, results)
    finally:
        browser.get_driver().quit()


results = {}
threads_num = 2

threads = [threading.Thread(target=func, args=(n, threads_num, results)) for n in range(threads_num)]
[t.start() for t in threads]
[t.join() for t in threads]

print("successful threads:", len(results))

