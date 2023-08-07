import threading
import multiprocessing

from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from pages.main_page import MainPage


def get_driver():
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)
    driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


class ScrapeThread(threading.Thread):
    def __init__(self, main_page, start, stop, step=1):
        threading.Thread.__init__(self)
        self.website = main_page
        self.start = start
        self.stop = stop
        self.step = step

    def run(self):
        self.website.get_pages_data_in_range(start=self.start, stop=self.stop, step=self.step)


class ScrapeProcess(multiprocessing.Process):
    def __init__(self, main_page, start, stop, step=1):
        multiprocessing.Process.__init__(self)
        self.website = main_page
        self.start = start
        self.stop = stop
        self.step = step

    def run(self):
        self.website.get_pages_data_in_range(start=self.start, stop=self.stop, step=self.step)
        print(len(self.website.database))


def browser_function():
    threads_num = 2
    websites = [MainPage(driver=get_driver()) for i in range(threads_num)]

    threads = []

    [ScrapeProcess(websites[i], start=i+1, stop=7, step=threads_num) for i in range(len(websites))]
    [t.start() for t in threads]
    [t.join() for t in threads]


if __name__ == "__main__":
    browser_function()
