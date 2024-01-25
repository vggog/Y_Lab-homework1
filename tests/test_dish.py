from starlette import status

from .conftest import client
from src.dish.repository import Repository
from src.menu.repository import Repository as MenuRepository


menu_data = {
    "title": "menu",
    "description": "description of menu",
}

submenu_data = {
    "title": "submenu",
    "description": "description of submenu",
}

dish_data = {
    "price": "12.50",
    "title": "submenu",
    "description": "description of submenu",
}


def setup_module():
    """
    Создание меню и сабменю, к которому принадлежит блюдо.
    :return:
    """
    response = client.post(
        "/menus",
        json=menu_data,
    )
    menu_id = response.json()["id"]

    response = client.post(
        f"/menus/{menu_id}/submenus",
        json=submenu_data
    )

    submenu_id = response.json()["id"]

    menu_data["id"] = menu_id
    submenu_data["id"] = submenu_id


def test_get_all_dishes():
    """
    Тест ручки для получения всех блюд определённого сабменю
    :return:
    """
    menu_id = menu_data["id"]
    submenu_id = submenu_data["id"]

    response = client.get(f"/menus/{menu_id}/submenus/{submenu_id}/dishes")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_create_dish(
        repo: Repository = Repository(),
):
    """
    Тест для создания блюда.
    :return:
    """
    menu_id = menu_data["id"]
    submenu_id = submenu_data["id"]

    response = client.post(
        f"/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json=dish_data,
    )

    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()

    assert response_data["title"] == dish_data["title"]
    assert response_data["description"] == dish_data["description"]
    assert response_data["price"] == dish_data["price"]

    dish_id = response_data["id"]
    dish_data["id"] = dish_id
    dish = repo.get_by_id(dish_id)

    assert dish.title == dish_data["title"]
    assert dish.description == dish_data["description"]
    assert dish.price == dish_data["price"]


def test_get_dish():
    """
    Тест ручки для получения определённого блюда.
    :return:
    """
    menu_id = menu_data["id"]
    submenu_id = submenu_data["id"]
    dish_id = dish_data["id"]

    response = client.get(
        f"/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}"
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert response_data["id"] == dish_data["id"]
    assert response_data["title"] == dish_data["title"]
    assert response_data["description"] == dish_data["description"]
    assert response_data["price"] == dish_data["price"]


def test_update_title_of_dish(
        repo: Repository = Repository(),
):
    """
    Тест ручки для обновления блюда.
    Обновление названия(title).
    :return:
    """
    menu_id = menu_data["id"]
    submenu_id = submenu_data["id"]
    dish_id = dish_data["id"]

    updated_title = {
        "title": "updated title of dish"
    }

    response = client.patch(
        f"/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
        json=updated_title,
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert response_data["id"] == dish_data["id"]
    assert response_data["title"] == updated_title["title"]
    assert response_data["description"] == dish_data["description"]
    assert response_data["price"] == dish_data["price"]

    dish = repo.get_by_id(dish_id)

    assert dish.title == updated_title["title"]
    assert dish.description == dish_data["description"]
    assert dish.price == dish_data["price"]

    dish_data["title"] = updated_title["title"]


def test_update_description_of_dish(
        repo: Repository = Repository(),
):
    """
    Тест ручки для обновления блюда.
    Обновление описания(description).
    :return:
    """
    menu_id = menu_data["id"]
    submenu_id = submenu_data["id"]
    dish_id = dish_data["id"]

    updated_description = {
        "description": "updated description of dish"
    }

    response = client.patch(
        f"/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
        json=updated_description,
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert response_data["id"] == dish_data["id"]
    assert response_data["title"] == dish_data["title"]
    assert response_data["description"] == updated_description["description"]
    assert response_data["price"] == dish_data["price"]

    dish = repo.get_by_id(dish_id)

    assert dish.title == dish_data["title"]
    assert dish.description == updated_description["description"]
    assert dish.price == dish_data["price"]

    dish_data["description"] = updated_description["description"]


def test_update_price_of_dish(
        repo: Repository = Repository(),
):
    """
    Тест ручки для обновления блюда.
    Обновление цены(price).
    :return:
    """
    menu_id = menu_data["id"]
    submenu_id = submenu_data["id"]
    dish_id = dish_data["id"]

    updated_price = {
        "price": "15.30"
    }

    response = client.patch(
        f"/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
        json=updated_price,
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert response_data["id"] == dish_data["id"]
    assert response_data["title"] == dish_data["title"]
    assert response_data["description"] == dish_data["description"]
    assert response_data["price"] == updated_price["price"]

    dish = repo.get_by_id(dish_id)

    assert dish.title == dish_data["title"]
    assert dish.description == dish_data["description"]
    assert dish.price == updated_price["price"]

    dish_data["price"] = updated_price["price"]


def test_update_dish(
        repo: Repository = Repository(),
):
    """
    Тест ручки для обновления блюда.
    Обновление всех полей: название(title), описания(description), цена(price).
    :return:
    """
    menu_id = menu_data["id"]
    submenu_id = submenu_data["id"]
    dish_id = dish_data["id"]

    updated_dish = {
        "title": "twice updated title of dish",
        "description": "twice updated description of dish",
        "price": "98.30",
    }

    response = client.patch(
        f"/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
        json=updated_dish,
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert response_data["id"] == dish_data["id"]
    assert response_data["title"] == updated_dish["title"]
    assert response_data["description"] == updated_dish["description"]
    assert response_data["price"] == updated_dish["price"]

    dish = repo.get_by_id(dish_id)

    assert dish.title == updated_dish["title"]
    assert dish.description == updated_dish["description"]
    assert dish.price == updated_dish["price"]


def test_delete_dish(
        repo: Repository = Repository()
):
    """
    Тест ручки для удаления блюда.
    """
    menu_id = menu_data["id"]
    submenu_id = submenu_data["id"]
    dish_id = dish_data["id"]

    response = client.delete(
        f"/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}"
    )

    assert response.status_code == status.HTTP_200_OK
    submenu = repo.get_by_id(dish_id)

    assert not submenu


def teardown_module():
    """
    Удаление созданных меню и сабменю.
    :return:
    """
    repo: MenuRepository = MenuRepository()
    menu_id = menu_data["id"]

    repo.delete(menu_id)
