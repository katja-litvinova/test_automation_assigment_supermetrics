from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(browser, 10)

    def is_element_present(self, how: str, what: str) -> bool:
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            raise ValueError(f"Can't navigate on the page. Check page elements naming.")
        return True

    def is_element_not_present(self, how: str, what: str) -> bool:
        try:
            element = self.browser.find_element(how, what)
            if element:
                raise AssertionError("Element is presented. But shouldn't")
        except NoSuchElementException:
            return True

    def wait_for_element_present(self, locator: tuple[str]) -> None:
        try:
            self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise ValueError("Can't navigate on the page. Check page elements naming.")
