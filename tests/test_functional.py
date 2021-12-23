import pytest
from pages.pages import LoginPage as LP
from pages.pages import KittyPage as KP

admin = "admin", "adminpass"
user = "user", "helloworld"


def test_login_page(browser):
    LP(browser).should_be_login_page()


@pytest.mark.parametrize(("username", "password"), [admin, user])
def test_cats_info(browser, username, password):
    expected_cat_info = [
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


@pytest.mark.parametrize(("username", "password"), [admin, user])
def test_awesomeness(browser, username, password):
    LP(browser).login(username, password)
    KP(browser).reset_data()
    KP(browser).validate_awesomeness()
    KP(browser).logout()


@pytest.mark.parametrize(("username", "password"), [admin, user])
def test_order_of_awesomeness(browser, username, password):
    LP(browser).login(username, password)
    KP(browser).reset_data()
    KP(browser).validate_awesomeness_order()
    KP(browser).logout()


def test_delete_cat_admin(browser):
    LP(browser).login("admin", "adminpass")
    try:
        KP(browser).validate_cats_deletion()
    finally:
        KP(browser).reset_data()
    KP(browser).logout()


def test_delete_unavailable(browser):
    LP(browser).login("user", "helloworld")
    KP(browser).validate_cats_deletion_unavailable()
    KP(browser).logout()


@pytest.mark.parametrize(("username", "password"), [admin, user])
def test_rename_cat(browser, username, password):
    new_name = "Kate"
    LP(browser).login(username, password)
    KP(browser).rename_cat_name(new_name)
    try:
        KP(browser).validate_new_cat_name(new_name)
    finally:
        KP(browser).reset_data()
    KP(browser).logout()


@pytest.mark.parametrize(("username", "password"), [admin, user])
def test_rename_cat_unavailable(browser, username, password):
    LP(browser).login(username, password)
    try:
        KP(browser).validate_rename_cat_unavailable()
    finally:
        KP(browser).reset_data()
    KP(browser).logout()


def test_changes_persisted(browser):
    new_name = "Kate"
    LP(browser).login("user", "helloworld")
    KP(browser).rename_cat_name(new_name)
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
