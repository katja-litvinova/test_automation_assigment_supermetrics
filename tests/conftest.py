import pytest as pytest
import selenium.webdriver as webdriver

HOST = "http://localhost:3000/"


@pytest.fixture(scope="function")
def browser():
    browser = webdriver.Chrome()
    browser.get(HOST)
    yield browser
    browser.quit()
