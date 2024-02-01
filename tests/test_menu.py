from starlette import status

from .conftest import client


menu_data = {
    "title": "menu 1",
    "description": "description of menu 1",
}


def test_get_all_menus():
    """
    Тест ручки для получения всех меню.
    :return:
    """
    response = client.get("/menus")
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 0


def test_add_menus():
    """
    Тест ручки для создания меню.
    :return:
    """
    response = client.post(
        "/menus",
        json=menu_data,
    )
    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    assert response_data.get("id")
    assert response_data.get("title")
    assert response_data.get("description")

    assert response_data["title"] == menu_data["title"]
    assert response_data["description"] == menu_data["description"]

    response = client.get("/menus")
    assert response.status_code == status.HTTP_200_OK

    get_all_response_data = response.json()
    assert isinstance(get_all_response_data, list)
    assert len(get_all_response_data) == 1

    menu_data["id"] = response_data["id"]


def test_get_menu():
    """
    Тест ручки для получения конкретного меню.
    :return:
    """
    menu_id = menu_data["id"]
    response = client.get(f"/menus/{ menu_id}")
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data.get("id")
    assert response_data.get("title")
    assert response_data.get("description")

    assert response_data["title"] == menu_data["title"]
    assert response_data["description"] == menu_data["description"]


def test_update_title_of_menu():
    """
    Тест ручки для обновления меню.
    Обновления названия(title).
    :return:
    """
    updated_title = {
        "title": "update menu 1"
    }

    menu_id = menu_data["id"]
    response = client.patch(
        f"/menus/{ menu_id}",
        json=updated_title,
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert response_data["title"] == updated_title["title"]
    assert response_data["description"] == menu_data["description"]

    menu_data["title"] = updated_title["title"]


def test_update_description_of_menu():
    """
    Тест ручки для обновления меню.
    Обновления описания(description).
    :return:
    """
    updated_description = {
        "description": "updated description of menu 1"
    }

    menu_id = menu_data["id"]
    response = client.patch(
        f"/menus/{ menu_id}",
        json=updated_description,
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert response_data["title"] == menu_data["title"]
    assert response_data["description"] == updated_description["description"]

    menu_data["description"] = updated_description["description"]


def test_update_menu():
    """
    Тест ручки для обновления меню.
    Обновление названия(title) и описания(description).
    :return:
    """
    updated_menu = {
        "title": "twice updated of menu 1",
        "description": "twice updated description of menu 1",
    }

    menu_id = menu_data["id"]
    response = client.patch(
        f"/menus/{ menu_id}",
        json=updated_menu,
    )

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data.get("id")
    assert response_data.get("title")
    assert response_data.get("description")

    assert response_data["title"] == updated_menu["title"]
    assert response_data["description"] == updated_menu["description"]

    menu_data["title"] = updated_menu["title"]
    menu_data["description"] = updated_menu["description"]


def test_delete_menu():
    """
    Тест ручки для удаления меню.
    :return:
    """
    menu_id = menu_data["id"]
    response = client.delete(f"/menus/{ menu_id}")
    assert response.status_code == status.HTTP_200_OK

    response = client.get(f"/menus/{ menu_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = client.get("/menus")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 0
