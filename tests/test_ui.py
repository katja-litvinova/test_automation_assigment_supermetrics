import time
import pytest

from testlib.base_page import BasePage
from testlib.locators import KittyPageLocators
from testlib.pages import LoginPage as LP, sum_of_ascii_symbols
from testlib.pages import KittyPage as KP

ADMIN: tuple[str, str] = "admin", "adminpass"
USER: tuple[str, str] = "user", "helloworld"


@pytest.fixture(autouse=True)
def reset_and_logout(browser):
    yield
    KP(browser).reset_data()
    KP(browser).logout()


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
    assert actual_cats_info == expected_cat_info


@pytest.mark.parametrize(("username", "password"), [ADMIN, USER])
def test_calculation_of_awesomeness(browser, username, password):
    LP(browser).login(username, password)
    KP(browser).reset_data()
    cat_names = KP(browser).get_cats_names()
    sum_ascii_for_cats_name = [
        str(sum_of_ascii_symbols(cat_name)) if cat_name != "James" else "∞"
        for cat_name in cat_names
    ]
    awesomeness_from_page = KP(browser).get_awesomeness_from_all_cats()
    assert awesomeness_from_page == sum_ascii_for_cats_name


@pytest.mark.parametrize(("username", "password"), [ADMIN, USER])
def test_order_of_awesomeness(browser, username, password):
    LP(browser).login(username, password)
    KP(browser).reset_data()
    actual_awesomeness = KP(browser).get_awesomeness_from_all_cats()
    expected_awesomeness = sorted(actual_awesomeness, reverse=True)
    assert actual_awesomeness == expected_awesomeness


def test_delete_first_cat_by_admin(browser):
    LP(browser).login("admin", "adminpass")
    first_cat_name_before_deletion = KP(browser).get_first_cat_name()
    KP(browser).delete_first_cat()
    time.sleep(0.5)
    first_cat_name_after_deletion = KP(browser).get_first_cat_name()
    assert (
            first_cat_name_before_deletion != first_cat_name_after_deletion
        ), "The first cat has not been deleted."


def test_delete_button_unavailable_login_by_user(browser):
    LP(browser).login("user", "helloworld")
    BasePage(browser).is_element_not_present(*KittyPageLocators.DELETE_BUTTON)


@pytest.mark.parametrize(("username", "password"), [ADMIN, USER])
def test_rename_first_cat(browser, username, password):
    new_name: str = "Kate"
    LP(browser).login(username, password)
    KP(browser).rename_first_cat(new_name)
    KP(browser).save_cat_name()
    cat_names = KP(browser).get_cats_names()
    assert (
            new_name in cat_names
        ), f"The new {new_name} is not presented in the page.\nCurrent cats' names:{cat_names}"


@pytest.mark.parametrize(("username", "password"), [ADMIN, USER])
def test_rename_first_cat_to_existed_name(browser, username, password):
    LP(browser).login(username, password)
    cat_names = KP(browser).get_cats_names()
    new_cat_name_from_second_cat = cat_names[1]
    KP(browser).rename_first_cat(new_cat_name_from_second_cat)
    BasePage(browser).is_element_present(*KittyPageLocators.SAVE_BTN_NOT_ALLOWED)


def test_changes_between_logins(browser):
    new_name: str = "Kate"
    LP(browser).login("user", "helloworld")
    KP(browser).rename_first_cat(new_name)
    KP(browser).save_cat_name()
    time.sleep(0.5)
    first_visit = KP(browser).get_whole_kitty_info()
    KP(browser).logout()
    LP(browser).login("user", "helloworld")
    second_visit = KP(browser).get_whole_kitty_info()
    assert (
            second_visit == first_visit
        ), "Changes to the cat should be persisted between visits to the app."
