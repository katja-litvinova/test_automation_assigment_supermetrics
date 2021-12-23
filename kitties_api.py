import requests

base_url = "http://localhost:3000/api"


def login(login_data: dict[str]) -> requests.Response:
    return requests.post(base_url + "/register", data=login_data)


def kitties_data(auth_data: dict[str]) -> requests.Response:
    return requests.get(base_url + "/kitties", headers=auth_data)


def rename_cat(auth_data: dict[str], old_name: str, new_name: dict[str]) -> requests.Response:
    return requests.put(
        base_url + f"/kitties/{old_name}", headers=auth_data, data=new_name
    )


def delete_cat(auth_data: dict[str], name: str) -> requests.Response:
    return requests.delete(base_url + f"/kitties/{name}", headers=auth_data)


def reset_changes() -> requests.Response:
    return requests.get(base_url + "/reset")
