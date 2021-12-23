import pytest

from kitties_api import *

auth_admin = {"Authorization": "Bearer adminToken"}
auth_user = {"Authorization": "Bearer userToken"}


def test_login_missing():
    login_data_missing = {"username": "admin", "password": ""}
    response = login(login_data_missing)
    assert (
        response.status_code == 400
    ), f"Status code is wrong, expected 400, got {response.status_code}"
    assert "Missing username or password" in response.text


def test_login_incorrect():
    login_data_incorrect = {"username": "hello", "password": "there"}
    response = login(login_data_incorrect)
    assert (
        response.status_code == 401
    ), f"Status code is wrong, expected 401, got {response.status_code}"
    assert "Incorrect username or password" in response.text


def test_login_admin():
    login_data_admin = {"username": "admin", "password": "adminpass"}
    response = login(login_data_admin)
    assert (
        response.status_code == 200
    ), f"Status code is wrong, expected 200, got {response.status_code}"
    assert "adminToken" in response.text


def test_login_user():
    login_data_user = {"username": "user", "password": "helloworld"}
    response = login(login_data_user)
    assert (
        response.status_code == 200
    ), f"Status code is wrong, expected 200, got {response.status_code}"
    assert "userToken" in response.text


def test_kitties_info():
    kitties_info = [
        {"name": "Otto", "pictureUrl": "https://placekitten.com/200/300?image=1"},
        {"name": "James", "pictureUrl": "https://placekitten.com/200/300?image=2"},
        {"name": "Sergey", "pictureUrl": "https://placekitten.com/200/300?image=3"},
        {"name": "Harri", "pictureUrl": "https://placekitten.com/200/300?image=4"},
        {"name": "Dups", "pictureUrl": "https://placekitten.com/200/300?image=5"},
        {"name": "Peter", "pictureUrl": "https://placekitten.com/200/300?image=6"},
    ]

    response = kitties_data(auth_admin)
    assert (
        response.status_code == 200
    ), f"Status code is wrong, expected 200, got {response.status_code}"
    assert response.json() == kitties_info


@pytest.mark.parametrize("auth", [auth_admin, auth_user])
def test_rename_cat(auth):
    data_new_name = {"newName": "Kate"}
    response = rename_cat(auth, "Otto", data_new_name)
    try:
        assert (
            response.status_code == 200
        ), f"Status code is wrong, expected 200, got {response.status_code}"
    finally:
        reset_changes()


@pytest.mark.parametrize("auth", [auth_admin, auth_user])
def test_rename_cat_admin_invalid(auth):
    invalid_data_new_name = {"newName": ""}
    response = rename_cat(auth, "Otto", invalid_data_new_name)
    try:
        assert (
            response.status_code == 400
        ), f"Status code is wrong, expected 400, got {response.status_code}"
        assert "Required parameter 'newName' missing" in response.text
    finally:
        reset_changes()


def test_delete_cat_admin():
    response = delete_cat(auth_admin, "Sergey")
    try:
        assert (
            response.status_code == 200
        ), f"Status code is wrong, expected 200, got {response.status_code}"
    finally:
        reset_changes()


def test_delete_cat_admin_invalid():
    response = delete_cat(auth_admin, "Christmas")
    try:
        assert (
            response.status_code == 400
        ), f"Status code is wrong, expected 400, got {response.status_code}"
        assert "Unknown kitty requested to be deleted" in response.text
    finally:
        reset_changes()


def test_delete_cat_user():
    response = delete_cat(auth_user, "Harri")
    try:
        assert (
            response.status_code == 400
        ), f"Status code is wrong, expected 400, got {response.status_code}"
    finally:
        reset_changes()
