from pages.base_page import BasePage
from pages.locators import KittyPageLocators, CommonLocators, LoginPageLocators

CatInfo = dict[str, str]


def sum_of_ascii_symbols(cat_name: str) -> int:
    lst = [ord(letters_in_cat_name) for letters_in_cat_name in cat_name]
    return sum(lst)


def raw_cats_info_to_dict(raw_cats_info: list[str]) -> CatInfo:
    iter_el = iter(raw_cats_info)
    return dict(zip(iter_el, iter_el))


def clean_text(raw_elements: list[str]) -> list[str]:
    return [el.replace(":", "") for el in raw_elements]


class LoginPage(BasePage, LoginPageLocators):
    def login(self, username: str, password: str) -> None:
        self.wait_for_element_present(LoginPageLocators.USERNAME_FIELD)
        self.browser.find_element(*LoginPageLocators.USERNAME_FIELD).send_keys(username)
        self.browser.find_element(*LoginPageLocators.PASSWORD_FIELD).send_keys(password)
        self.browser.find_element(*LoginPageLocators.LOGIN_BUTTON).click()


class KittyPage(BasePage, KittyPageLocators):
    def get_whole_kitty_info(self) -> list[CatInfo]:
        self.wait_for_element_present(KittyPageLocators.ALL_CATS_INFO)
        cats = self.browser.find_elements(*KittyPageLocators.ALL_CATS_INFO)
        actual_cats_information: list[CatInfo] = []
        for cat in cats:
            raw_text: list[str] = cat.text.split("\n")
            cleaned_text = clean_text(raw_text)
            name = cleaned_text.pop()
            cat_info = raw_cats_info_to_dict(cleaned_text)
            cat_info["Name"] = name
            actual_cats_information.append(cat_info)
        return actual_cats_information

    def get_awesomeness(self) -> list[str]:
        self.wait_for_element_present(KittyPageLocators.ALL_CATS_INFO)
        cats_awesomeness = self.browser.find_elements(
            *KittyPageLocators.CAT_AWESOMENESS
        )
        return [awesome.text for awesome in cats_awesomeness]

    def get_first_cat_name(self) -> str:
        self.wait_for_element_present(KittyPageLocators.ALL_CATS_INFO)
        return self.browser.find_element(*KittyPageLocators.CAT_NAME).text

    def get_cat_names(self) -> list[str]:
        self.wait_for_element_present(KittyPageLocators.ALL_CATS_INFO)
        cats_name = self.browser.find_elements(*KittyPageLocators.CAT_NAME)
        return [name.text for name in cats_name]

    def rename_cat_name(self, new_name: str) -> None:
        self.wait_for_element_present(KittyPageLocators.CAT_NAME)
        cat_name = self.browser.find_element(*KittyPageLocators.CAT_NAME)
        cat_name.click()
        cat_name.clear()
        cat_name.send_keys(new_name)

    def save_cat_name(self) -> None:
        self.wait_for_element_present(KittyPageLocators.SAVE_BTN_ENABLED)
        save = self.browser.find_element(*KittyPageLocators.SAVE_BUTTON)
        save.click()

    def delete_cat(self) -> None:
        self.wait_for_element_present(KittyPageLocators.DELETE_BUTTON)
        cat_del = self.browser.find_element(*KittyPageLocators.DELETE_BUTTON)
        cat_del.click()

    def reset_data(self) -> None:
        self.wait_for_element_present(CommonLocators.RESET_BUTTON)
        self.browser.find_element(*CommonLocators.RESET_BUTTON).click()

    def logout(self) -> None:
        self.wait_for_element_present(KittyPageLocators.LOGOUT_BUTTON)
        self.browser.find_element(*KittyPageLocators.LOGOUT_BUTTON).click()
