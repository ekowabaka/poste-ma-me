from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pyautogui
import time
import sys


def ensure_login(func):
    """
    Decorator to ensure that logins are enforced before any other actions
    :param func:
    :return:
    """

    def enforcer(instance, image_path, message, expand=True):
        if WebUIInterface.logged_in:
            func(instance, image_path, message, expand)
        else:
            print("You are currently not logged in!", file=sys.stderr)

    return enforcer


class Dummy(object):
    def __init__(self, username, password, headless=False):
        pass

    def login(self):
        print("Logging in")

    def post(self, image_path, message, expand=True):
        print("Posting", image_path)
        print("Message", message)


class WebUIInterface(object):

    logged_in = False

    def get_firefox(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference(
            "general.useragent.override",
            "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) "
            "Chrome/18.0.1025.133 Mobile Safari/535.19 "
        )
        return webdriver.Firefox(profile)

    def get_chrome(self):
        options = Options()
        userAgent = "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, " \
                    "like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19 "
        options.add_argument("user-agent=%s" % userAgent)
        return webdriver.Chrome(chrome_options=options)

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
        self.browser = self.get_firefox()
        self.browser.implicitly_wait(10)
        self.browser.set_window_size(400, 850)
        self.browser.get("http://instagram.com")

        element = self.browser.find_element_by_xpath("//button[text()='Log In']")
        element.click()
        time.sleep(1)

        element = self.browser.find_element_by_name("username")
        element.send_keys(self.username)

        element = self.browser.find_element_by_name("password")
        element.send_keys(self.password)

        element = self.browser.find_element_by_xpath("//div[text()='Log In']")
        element.click()
        time.sleep(15)

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
                time.sleep(5)
                WebUIInterface.logged_in = True
            except NoSuchElementException:
                WebUIInterface.logged_in = False
                raise ConnectionError("Logging into instagram failed!")

    @ensure_login
    def post(self, image_path, message, expand=True):
        """
        Post an image and its message
        :param image_path:
        :param message:
        :param expand:
        :return:
        """
        element = self.browser.find_element_by_xpath("//span[@aria-label='New Post']")
        element = element.find_element_by_xpath("./..")
        element.click()
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'l')

        pyautogui.typewrite(image_path)
        time.sleep(20)
        pyautogui.press('enter')

        time.sleep(20)

        if expand:
            element = self.browser.find_element_by_xpath("//span[text()='Expand']")
            element = element.find_element_by_xpath("./..")
            element.click()

        time.sleep(20)

        element = self.browser.find_element_by_xpath("//button[text()='Next']")
        element.click()

        time.sleep(20)

        element = self.browser.find_element_by_xpath("//textarea[@placeholder='Write a caption…']")
        element.send_keys(message)

        time.sleep(20)

        element = self.browser.find_element_by_xpath("//button[text()='Share']")
        element.click()




