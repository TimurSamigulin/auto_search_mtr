from selenium import webdriver

class Driver():

    def __init__(self, headless=True):
        firefox_options = webdriver.FirefoxOptions()
        if headless:
            firefox_options.add_argument('-headless')

        self.driver = webdriver.Firefox(options=firefox_options)

    def get_driver(self):
        return self.driver

    def close_driver(self):
        self.driver.quit()
