from selenium.webdriver.common.by import By


class CommonLocators(object):
    RESET_BUTTON = (By.XPATH, "//div/button[contains(.,'Reset')]")


class LoginPageLocators(object):
    LOGIN_FORM = (By.XPATH, "//*[local-name() = 'form']")
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")


class KittyPageLocators(object):
    LOGOUT_BUTTON = (By.XPATH, "//button[text()='Log out']")
    CAT_NAME = (By.XPATH, "//div[@contenteditable]")
    CAT_RANK = (By.XPATH, "//div[child::span[contains(.,'Rank')]]/span[2]")
    CAT_AWESOMENESS = (By.XPATH, "//div[child::span[contains(.,'Rank')]]/span[4]")
    ALL_CATS_INFO = (By.XPATH, "//div[child::div/child::span[contains(.,'Rank')]]")
    DELETE_BUTTON = (By.XPATH, "//*[local-name() = 'svg'][2]")
    SAVE_BUTTON = (By.XPATH, "//*[local-name() = 'svg'][1]")
    SAVE_BTN_ENABLED = (By.XPATH, "//*[local-name()='svg' and @stroke='green']")
    SAVE_BTN_NOT_ALLOWED = (By.XPATH, "//*[local-name()='svg' and @stroke='red']")
