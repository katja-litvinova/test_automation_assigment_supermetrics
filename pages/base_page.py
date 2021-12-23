from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage(object):
    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(browser, 10)

    def is_element_present(self, how, what):
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            raise ValueError("Can't navigate on the page. Check page elements naming.")
        return True

    def wait_for_element_present(self, locator):
        try:
            self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise ValueError("Can't navigate on the page. Check page elements naming.")
