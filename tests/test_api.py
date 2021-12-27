import pytest
import requests
from http import HTTPStatus
from testlib.kitties_api import (
    login,
    get_kitties_data,
    rename_cat,
    delete_cat,
    reset_changes,
)

AUTH_ADMIN: dict[str, str] = {"Authorization": "Bearer adminToken"}
AUTH_USER: dict[str, str] = {"Authorization": "Bearer userToken"}

LOGIN_ADMIN: dict[str, str] = {"username": "admin", "password": "adminpass"}
LOGIN_USER: dict[str, str] = {"username": "user", "password": "helloworld"}

PASSWORD_MISSING: dict[str, str] = {"username": "admin", "password": ""}
ERROR_MISSING: str = "Missing username or password"

CREDENTIALS_INCORRECT: dict[str, str] = {"username": "hello", "password": "there"}
ERROR_INCORRECT: str = "Incorrect username or password"

CONNECTION_ERROR: str = "Connection refused"


@pytest.fixture(autouse=True)
def reset():
    yield
    reset_changes()


@pytest.mark.parametrize(
    "auth, message", [(LOGIN_ADMIN, "adminToken"), (LOGIN_USER, "userToken")]
)
def test_login_valid(auth, message):
    response = login(auth)
    assert isinstance(response, requests.Response), CONNECTION_ERROR
    assert response.status_code == HTTPStatus.OK
    assert message in response.text


@pytest.mark.parametrize(
    "auth, status_code, message",
    [
        (PASSWORD_MISSING, HTTPStatus.BAD_REQUEST, ERROR_MISSING),
        (CREDENTIALS_INCORRECT, HTTPStatus.UNAUTHORIZED, ERROR_INCORRECT),
    ],
)
def test_login_invalid(auth, status_code, message):
    response = login(auth)
    assert isinstance(response, requests.Response), CONNECTION_ERROR
    assert response.status_code == status_code
    assert message in response.text


def test_kitties_info():
    kitties_info: list[dict[str, str]] = [
        {"name": "Otto", "pictureUrl": "https://placekitten.com/200/300?image=1"},
        {"name": "James", "pictureUrl": "https://placekitten.com/200/300?image=2"},
        {"name": "Sergey", "pictureUrl": "https://placekitten.com/200/300?image=3"},
        {"name": "Harri", "pictureUrl": "https://placekitten.com/200/300?image=4"},
        {"name": "Dups", "pictureUrl": "https://placekitten.com/200/300?image=5"},
        {"name": "Peter", "pictureUrl": "https://placekitten.com/200/300?image=6"},
    ]

    response = get_kitties_data(AUTH_ADMIN)
    assert isinstance(response, requests.Response), CONNECTION_ERROR
    assert response.status_code == HTTPStatus.OK
    assert response.json() == kitties_info


@pytest.mark.parametrize("auth", [AUTH_ADMIN, AUTH_USER])
def test_rename_cat(auth):
    new_name: dict[str, str] = {"newName": "Kate"}
    response = rename_cat(auth, "Otto", new_name)
    assert isinstance(response, requests.Response), CONNECTION_ERROR
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize("auth", [AUTH_ADMIN, AUTH_USER])
def test_rename_cat_required_parameter_missing(auth):
    invalid_data_new_name: dict[str, str] = {"newName": ""}
    response = rename_cat(auth, "Otto", invalid_data_new_name)
    assert isinstance(response, requests.Response), CONNECTION_ERROR
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "Required parameter 'newName' missing" in response.text


def test_delete_cat_by_admin():
    response = delete_cat(AUTH_ADMIN, "Sergey")
    assert isinstance(response, requests.Response), CONNECTION_ERROR
    assert response.status_code == HTTPStatus.OK


def test_delete_non_existent_cat():
    response = delete_cat(AUTH_ADMIN, "Christmas")
    assert isinstance(response, requests.Response), CONNECTION_ERROR
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "Unknown kitty requested to be deleted" in response.text


def test_delete_cat_by_user():
    response = delete_cat(AUTH_USER, "Harri")
    assert isinstance(response, requests.Response), CONNECTION_ERROR
    assert response.status_code == HTTPStatus.UNAUTHORIZED
