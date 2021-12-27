from typing import Optional
from urllib.parse import urljoin

import requests
from requests import Response, exceptions

BASE_URL = "http://localhost:3000/api/"


def check_connection(function):
    def wrapper(*args, **kwargs):
        try:
            fun = function(*args, **kwargs)
        except exceptions.ConnectionError:
            return None
        return fun

    return wrapper


@check_connection
def login(login_data: dict[str, str]) -> Optional[Response]:
    return requests.post(urljoin(BASE_URL, "register"), data=login_data)


@check_connection
def get_kitties_data(auth_data: dict[str, str]) -> Optional[Response]:
    return requests.get(urljoin(BASE_URL, "kitties"), headers=auth_data)


@check_connection
def rename_cat(
    auth_data: dict[str, str], old_name: str, new_name: dict[str, str]
) -> Optional[Response]:
    return requests.put(
        urljoin(BASE_URL, f"kitties/{old_name}"), headers=auth_data, data=new_name
    )


@check_connection
def delete_cat(auth_data: dict[str, str], name: str) -> Optional[Response]:
    return requests.delete(urljoin(BASE_URL, f"kitties/{name}"), headers=auth_data)


@check_connection
def reset_changes() -> Optional[Response]:
    return requests.get(urljoin(BASE_URL, "reset"))
