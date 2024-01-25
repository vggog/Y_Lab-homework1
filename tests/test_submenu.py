from starlette import status

from .conftest import client
from src.submenu.repository import Repository
from src.menu.repository import Repository as MenuRepository


menu_data = {
    "title": "menu",
    "description": "description of menu",
}

submenu_data = {
    "title": "submenu",
    "description": "description of submenu",
}


def setup_module():
    """
    Создание меню, к которому будет принадлежать сабменю.
    :return:
    """
    response = client.post(
        "/menus",
        json=menu_data,
    )
    menu_data["id"] = response.json()["id"]


def test_get_all_submenus():
    """
    Тест ручки для получения всех сабменю.
    :return:
    """
    menu_id = menu_data["id"]
    response = client.get(f"/menus/{menu_id}/submenus")

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert isinstance(response_data, list)
    assert len(response_data) == 0


def test_create_submenu(
        repo: Repository = Repository()
):
    """
    Тест ручки для создания сабменю.
    """
    menu_id = menu_data["id"]
    response = client.post(
        f"/menus/{menu_id}/submenus",
        json=submenu_data
    )

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()

    assert response_data.get("id")
    assert response_data.get("title")
    assert response_data.get("description")

    assert response_data["title"] == submenu_data["title"]
    assert response_data["description"] == submenu_data["description"]

    submenu_id = response_data["id"]
    submenu_data["id"] = submenu_id
    submenu = repo.get_submenu(menu_id, submenu_id)

    assert submenu.title == submenu_data["title"]
    assert submenu.description == submenu_data["description"]


def test_get_submenu():
    """
    Тест ручки для получения сабменю.
    """
    menu_id = menu_data["id"]
    submenu_id = submenu_data["id"]

    response = client.get(f"/menus/{menu_id}/submenus/{submenu_id}")

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert response_data.get("id")
    assert response_data.get("title")
    assert response_data.get("description")

    assert response_data["id"] == submenu_data["id"]
    assert response_data["title"] == submenu_data["title"]
    assert response_data["description"] == submenu_data["description"]


def test_update_title_of_submenu(
        repo: Repository = Repository()
):
    """
    Тест ручки для обновления сабменю.
    Обновление названия(title).
    """
    menu_id = menu_data["id"]
    submenu_id = submenu_data["id"]

    updated_title = {
        "title": "updated title of submenu"
    }

    response = client.patch(
        f"/menus/{menu_id}/submenus/{submenu_id}",
        json=updated_title,
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert response_data["id"] == submenu_data["id"]
    assert response_data["title"] == updated_title["title"]
    assert response_data["description"] == submenu_data["description"]

    submenu = repo.get_submenu(menu_id, submenu_id)

    assert submenu.title == updated_title["title"]
    assert submenu.description == submenu_data["description"]

    submenu_data["title"] = updated_title["title"]


def test_update_description_of_submenu(
        repo: Repository = Repository()
):
    """
    Тест ручки для обновления сабменю.
    Обновление описания(description).
    """
    menu_id = menu_data["id"]
    submenu_id = submenu_data["id"]

    updated_description = {
        "description": "updated description of submenu"
    }

    response = client.patch(
        f"/menus/{menu_id}/submenus/{submenu_id}",
        json=updated_description,
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert response_data["id"] == submenu_data["id"]
    assert response_data["title"] == submenu_data["title"]
    assert response_data["description"] == updated_description["description"]

    submenu = repo.get_submenu(menu_id, submenu_id)

    assert submenu.title == submenu_data["title"]
    assert submenu.description == updated_description["description"]

    submenu_data["description"] = updated_description["description"]


def test_update_submenu(
        repo: Repository = Repository()
):
    """
    Тест ручки для обновления сабменю.
    Обновление названия(title) и описания(desciption).
    """
    menu_id = menu_data["id"]
    submenu_id = submenu_data["id"]

    updated_data = {
        "title": "twice updated title of submenu",
        "description": "twice updated description of submenu"
    }

    response = client.patch(
        f"/menus/{menu_id}/submenus/{submenu_id}",
        json=updated_data,
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert response_data["id"] == submenu_data["id"]
    assert response_data["title"] == updated_data["title"]
    assert response_data["description"] == updated_data["description"]

    submenu = repo.get_submenu(menu_id, submenu_id)

    assert submenu.title == updated_data["title"]
    assert submenu.description == updated_data["description"]


def test_delete_submenu(
        repo: Repository = Repository()
):
    """
    Тест ручки для удаления сабменю.
    """
    menu_id = menu_data["id"]
    submenu_id = submenu_data["id"]

    response = client.delete(f"/menus/{menu_id}/submenus/{submenu_id}")

    assert response.status_code == status.HTTP_200_OK
    submenu = repo.get_submenu(menu_id, submenu_id)

    assert not submenu


def teardown_module():
    """
    Удалить созданное меню.
    :return:
    """
    repo: MenuRepository = MenuRepository()
    menu_id = menu_data["id"]

    repo.delete(menu_id)