import time
import pytest

from pages.base_page import BasePage
from pages.locators import LoginPageLocators, KittyPageLocators
from pages.pages import LoginPage as LP, sum_of_ascii_symbols
from pages.pages import KittyPage as KP

ADMIN: tuple[str, str] = "admin", "adminpass"
USER: tuple[str, str] = "user", "helloworld"


def test_login_page(browser):
    BasePage(browser).wait_for_element_present(LoginPageLocators.LOGIN_FORM)


@pytest.mark.parametrize(("username", "password"), [ADMIN, USER])
def test_cats_information(browser, username, password):
    expected_cat_info: list[dict[str, str]] = [
        {"Name": "James", "Rank": "1", "Awesomeness": "∞"},
        {"Name": "Sergey", "Rank": "2", "Awesomeness": "623"},
        {"Name": "Peter", "Rank": "3", "Awesomeness": "512"},
        {"Name": "Harri", "Rank": "4", "Awesomeness": "502"},
        {"Name": "Otto", "Rank": "5", "Awesomeness": "422"},
        {"Name": "Dups", "Rank": "6", "Awesomeness": "412"},
    ]

    LP(browser).login(username, password)
    KP(browser).reset_data()
    actual_cats_info = KP(browser).get_whole_kitty_info()
    assert actual_cats_info == expected_cat_info, (
        f"Name, Rank or Awesomeness are not right.\n"
        f"Expected result:{expected_cat_info}\n"
        f"Actual result:{actual_cats_info}"
    )
    KP(browser).logout()


@pytest.mark.parametrize(("username", "password"), [ADMIN, USER])
def test_awesomeness(browser, username, password):
    LP(browser).login(username, password)
    KP(browser).reset_data()
    cat_names = KP(browser).get_cat_names()
    ascii_names = [
        str(sum_of_ascii_symbols(cat_name)) if cat_name != "James" else "∞"
        for cat_name in cat_names
    ]
    awesomeness = KP(browser).get_awesomeness()
    assert awesomeness == ascii_names
    KP(browser).logout()


@pytest.mark.parametrize(("username", "password"), [ADMIN, USER])
def test_order_of_awesomeness(browser, username, password):
    LP(browser).login(username, password)
    KP(browser).reset_data()
    actual_awesomeness = KP(browser).get_awesomeness()
    expected_awesomeness = sorted(actual_awesomeness, reverse=True)
    assert actual_awesomeness == expected_awesomeness
    KP(browser).logout()


def test_delete_cat_admin(browser):
    LP(browser).login("admin", "adminpass")
    cat_name_before_deletion = KP(browser).get_first_cat_name()
    KP(browser).delete_cat()
    time.sleep(0.5)
    cat_name_after_deletion = KP(browser).get_first_cat_name()
    try:
        assert (
            cat_name_before_deletion != cat_name_after_deletion
        ), "The first cat has not been deleted."
    finally:
        KP(browser).reset_data()
    KP(browser).logout()


def test_delete_unavailable(browser):
    LP(browser).login("user", "helloworld")
    try:
        BasePage(browser).is_element_not_present(*KittyPageLocators.DELETE_BUTTON)
    finally:
        KP(browser).logout()


@pytest.mark.parametrize(("username", "password"), [ADMIN, USER])
def test_rename_cat(browser, username, password):
    new_name: str = "Kate"
    LP(browser).login(username, password)
    KP(browser).rename_cat_name(new_name)
    KP(browser).save_cat_name()
    names_list = KP(browser).get_cat_names()
    try:
        assert (
            new_name in names_list
        ), f"The new {new_name} is not presented in the page.\nCurrent cats' names:{names_list}"
    finally:
        KP(browser).reset_data()
    KP(browser).logout()


@pytest.mark.parametrize(("username", "password"), [ADMIN, USER])
def test_rename_cat_unavailable(browser, username, password):
    LP(browser).login(username, password)
    current_cat_names = KP(browser).get_cat_names()
    new_cat_name = current_cat_names[1]
    KP(browser).rename_cat_name(new_cat_name)
    try:
        BasePage(browser).is_element_present(*KittyPageLocators.SAVE_BTN_NOT_ALLOWED)
    finally:
        KP(browser).reset_data()
    KP(browser).logout()


def test_changes_persisted(browser):
    new_name: str = "Kate"
    LP(browser).login("user", "helloworld")
    KP(browser).rename_cat_name(new_name)
    KP(browser).save_cat_name()
    first_visit = KP(browser).get_whole_kitty_info()
    KP(browser).logout()
    LP(browser).login("user", "helloworld")
    second_visit = KP(browser).get_whole_kitty_info()
    try:
        assert (
            second_visit == first_visit
        ), "Changes to the cat should be persisted between visits to the app."
    finally:
        KP(browser).reset_data()
    KP(browser).logout()
