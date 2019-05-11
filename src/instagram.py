from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import sys


def ensure_login(func):
    """
    Decorator to ensure that logins are enforced before any other actions
    :param func:
    :return:
    """

    def enforcer(instance, image_path, message):
        if WebUIInterface.logged_in:
            func(instance, image_path, message)
        else:
            print("You are currently not logged in!", file=sys.stderr)

    return enforcer


class WebUIInterface(object):

    logged_in = False

    def __init__(self, username, password, headless=False):
        """
        Create an instance of the instagram interface
        :param username:
        :param password:
        :param headless:
        """
        self.username = username
        self.password = password
        self.headless = headless
        self.browser = None

    def login(self):
        """
        Loginto the instagram web UI
        :return:
        """
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

        try:
            element = self.browser.find_element_by_xpath("//button[text()='Not Now']")
            element.click()
            element = self.browser.find_element_by_xpath("//span[@aria-label='Profile']")
            element = element.find_element_by_xpath("./..")
            element.click()
            WebUIInterface.logged_in = True
        except NoSuchElementException:
            try:
                element = self.browser.find_element_by_xpath("//span[@aria-label='Profile']")
                element = element.find_element_by_xpath("./..")
                element.click()
                WebUIInterface.logged_in = True
            except NoSuchElementException:
                WebUIInterface.logged_in = False
                raise ConnectionError("Logging into instagram failed!")

    @ensure_login
    def post(self, image_path, message):
        element = self.browser.find_element_by_xpath("//span[@aria-label='New Post']")
        element = element.find_element_by_xpath("./..")
        element.click()
        element = self.browser.find_elements_by_xpath("//input[@type='file']")
        for file in element:
            file.send_keys(image_path)
