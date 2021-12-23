import time
from selenium.common.exceptions import NoSuchElementException
from pages.base_page import BasePage
from pages.locators import KittyPageLocators, CommonLocators, LoginPageLocators


class LoginPage(BasePage, LoginPageLocators):
    def login(self, username, password) -> None:
        self.wait_for_element_present(LoginPageLocators.USERNAME_FIELD)
        self.browser.find_element(*LoginPageLocators.USERNAME_FIELD).send_keys(username)
        self.browser.find_element(*LoginPageLocators.PASSWORD_FIELD).send_keys(password)
        self.browser.find_element(*LoginPageLocators.LOGIN_BUTTON).click()

    def should_be_login_page(self) -> None:
        self.wait_for_element_present(LoginPageLocators.LOGIN_FORM)


class KittyPage(BasePage, KittyPageLocators):
    @staticmethod
    def sum_of_ascii(cat_name: str) -> int:
        lst = [ord(i) for i in str(cat_name)]
        return sum(lst)

    @staticmethod
    def convert_list_to_dict(lst: list) -> dict:
        res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
        return res_dct

    def get_whole_kitty_info(self) -> list[dict]:
        self.wait_for_element_present(KittyPageLocators.ALL_CATS_INFO)
        cats = self.browser.find_elements(*KittyPageLocators.ALL_CATS_INFO)
        actual_cats_info = []
        for cat in cats:
            get_text = cat.text.split("\n")
            last_element = get_text.pop()
            get_text.insert(0, "Name:")
            get_text.insert(1, last_element)
            dict_cat = self.convert_list_to_dict(get_text)
            dict_cat_changed = {k.replace(":", ""): v for k, v in dict_cat.items()}
            actual_cats_info.append(dict_cat_changed)
        return actual_cats_info

    def validate_awesomeness(self) -> None:
        self.wait_for_element_present(KittyPageLocators.ALL_CATS_INFO)
        cats = self.browser.find_elements(*KittyPageLocators.ALL_CATS_INFO)
        for cat in cats:
            get_text = cat.text.split("\n")
            take_name = get_text.pop()
            take_awesome = get_text.pop()
            convert_name = self.sum_of_ascii(take_name)
            if take_name == "James" and take_awesome == "∞":
                convert_name = "∞"
            assert (
                str(convert_name) == take_awesome
            ), f"Awesomeness is not right for the letters of the {take_name} name"

    def get_cat_names(self) -> list[str]:
        self.wait_for_element_present(KittyPageLocators.ALL_CATS_INFO)
        cats_name = self.browser.find_elements(*KittyPageLocators.CAT_NAME)
        all_names = [name.text for name in cats_name]
        return all_names

    def validate_awesomeness_order(self) -> None:
        self.wait_for_element_present(KittyPageLocators.ALL_CATS_INFO)
        cats_awesome = self.browser.find_elements(*KittyPageLocators.CAT_AWESOMENESS)
        actual_awesomeness = [awe.text for awe in cats_awesome]
        expected_awesomeness = sorted(actual_awesomeness, reverse=True)
        assert actual_awesomeness == expected_awesomeness, (
            f""
            f"The order of cat's awesomeness is not right."
            f"Expected result:{expected_awesomeness}\n"
            f"Actual result:{actual_awesomeness}"
        )

    def rename_cat_name(self, new_name: str) -> None:
        self.wait_for_element_present(KittyPageLocators.CAT_NAME)
        cat_name = self.browser.find_element(*KittyPageLocators.CAT_NAME)
        cat_name.click()
        cat_name.clear()
        cat_name.send_keys(new_name)
        self.wait_for_element_present(KittyPageLocators.SAVE_BTN_ENABLED)
        save = self.browser.find_element(*KittyPageLocators.SAVE_BUTTON)
        save.click()

    def validate_rename_cat_unavailable(self) -> None:
        current_cat_names = self.get_cat_names()
        new_cat_name = current_cat_names[1]
        cat_name = self.browser.find_element(*KittyPageLocators.CAT_NAME)
        cat_name.click()
        cat_name.clear()
        cat_name.send_keys(new_cat_name)
        self.is_element_present(*KittyPageLocators.SAVE_BTN_NOT_ALLOWED)

    def validate_new_cat_name(self, cat_name: str) -> None:
        names_list = self.get_cat_names()
        assert (
            cat_name in names_list
        ), f"The new {cat_name} is not presented in the page.\nCurrent cats' names:{names_list}"

    def delete_cat(self) -> None:
        self.wait_for_element_present(KittyPageLocators.DELETE_BUTTON)
        cat_del = self.browser.find_element(*KittyPageLocators.DELETE_BUTTON)
        cat_del.click()

    def validate_cats_deletion(self) -> None:
        cat_name_before_deletion = self.browser.find_element(*KittyPageLocators.CAT_NAME).text
        self.delete_cat()
        time.sleep(0.5)
        cat_name_after_deletion = self.browser.find_element(*KittyPageLocators.CAT_NAME).text
        assert cat_name_before_deletion != cat_name_after_deletion, (
            "The first cat has not been deleted."
        )

    def validate_cats_deletion_unavailable(self) -> None:
        try:
            del_button = self.browser.find_element(*KittyPageLocators.DELETE_BUTTON)
            if del_button:
                raise AssertionError("Delete button is presented. But shouldn't")
        except NoSuchElementException:
            print("Delete button is not presented")

    def reset_data(self) -> None:
        self.wait_for_element_present(CommonLocators.RESET_BUTTON)
        self.browser.find_element(*CommonLocators.RESET_BUTTON).click()

    def logout(self) -> None:
        self.wait_for_element_present(KittyPageLocators.LOGOUT_BUTTON)
        self.browser.find_element(*KittyPageLocators.LOGOUT_BUTTON).click()
