from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Interface(object):

    def __init__(self, username, password, headless=False):
        self.username = username
        self.password = password
        self.headless = headless
        self.browser = None

    def login(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference(
            "general.useragent.override",
            "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) "
            "Chrome/18.0.1025.133 Mobile Safari/535.19 "
        )
        self.browser = webdriver.Firefox(profile)
        self.browser.implicitly_wait(10)
        self.browser.set_window_size(400, 750)
        self.browser.get("http://instagram.com")

        element = self.browser.find_element_by_xpath("//button[text()='Log In']")
        element.click()

        element = self.browser.find_element_by_name("username")
        element.send_keys(self.username)

        element = self.browser.find_element_by_name("password")
        element.send_keys(self.password)

        element = self.browser.find_element_by_xpath("//div[text()='Log In']")
        element.click()

        element = self.browser.find_element_by_xpath("//button[text()='Not Now']")
        element.click()

