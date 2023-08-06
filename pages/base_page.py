class BasePage(object):

    url = None

    def __init__(self, driver):
        self.driver = driver
        self.database = []

    def go(self):
        self.driver.get(self.url)

    def set_url(self, new_url):
        self.url = new_url
