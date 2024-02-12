import pytest
from httpx import AsyncClient
from starlette import status

from main import app
from src.core.utils import reverse
from tests.conftest import sync_client

menu_data: dict[str, str] = {
    'title': 'menu',
    'description': 'description of menu',
}

submenu_data: dict[str, str] = {
    'title': 'submenu',
    'description': 'description of submenu',
}

dish_data: dict[str, str] = {
    'price': '12.50',
    'title': 'submenu',
    'description': 'description of submenu',
}


def setup_module():
    """
    Создание меню и сабменю, к которому принадлежит блюдо.
    :return:
    """
    response = sync_client.post(
        reverse(app, 'create_menu'),
        json=menu_data,
    )
    menu_id: str = response.json()['id']

    response = sync_client.post(
        reverse(app, 'create_submenu', menu_id=menu_id),
        json=submenu_data
    )

    submenu_id: str = response.json()['id']

    menu_data['id'] = menu_id
    submenu_data['id'] = submenu_id


@pytest.mark.asyncio
async def test_get_all_dishes(
        client: AsyncClient,
):
    """
    Тест ручки для получения всех блюд определённого сабменю
    :return:
    """
    menu_id: str = menu_data['id']
    submenu_id: str = submenu_data['id']

    response = await client.get(
        reverse(
            app,
            'get_all_dishes',
            menu_id=menu_id,
            submenu_id=submenu_id
        ),
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_dish(
        client: AsyncClient,
):
    """
    Тест для создания блюда.
    :return:
    """
    menu_id: str = menu_data['id']
    submenu_id: str = submenu_data['id']

    response = await client.post(
        reverse(
            app,
            'create_dish',
            menu_id=menu_id,
            submenu_id=submenu_id
        ),
        json=dish_data,
    )

    assert response.status_code == status.HTTP_201_CREATED

    response_data: dict[str, str] = response.json()

    assert response_data['title'] == dish_data['title']
    assert response_data['description'] == dish_data['description']
    assert response_data['price'] == dish_data['price']

    dish_id: str = response_data['id']
    dish_data['id'] = dish_id


@pytest.mark.asyncio
async def test_get_dish(
        client: AsyncClient,
):
    """
    Тест ручки для получения определённого блюда.
    :return:
    """
    menu_id: str = menu_data['id']
    submenu_id: str = submenu_data['id']
    dish_id: str = dish_data['id']

    response = await client.get(
        reverse(
            app,
            'get_dish',
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id
        ),
    )

    assert response.status_code == status.HTTP_200_OK
    response_data: dict[str, str] = response.json()

    assert response_data['id'] == dish_data['id']
    assert response_data['title'] == dish_data['title']
    assert response_data['description'] == dish_data['description']
    assert response_data['price'] == dish_data['price']


@pytest.mark.asyncio
async def test_update_title_of_dish(
        client: AsyncClient,
):
    """
    Тест ручки для обновления блюда.
    Обновление названия(title).
    :return:
    """
    menu_id: str = menu_data['id']
    submenu_id: str = submenu_data['id']
    dish_id: str = dish_data['id']

    updated_title: dict[str, str] = {
        'title': 'updated title of dish'
    }

    response = await client.patch(
        reverse(
            app,
            'update_dish',
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id
        ),
        json=updated_title,
    )

    assert response.status_code == status.HTTP_200_OK
    response_data: dict[str, str] = response.json()

    assert response_data['id'] == dish_data['id']
    assert response_data['title'] == updated_title['title']
    assert response_data['description'] == dish_data['description']
    assert response_data['price'] == dish_data['price']

    dish_data['title'] = updated_title['title']


@pytest.mark.asyncio
async def test_update_description_of_dish(
        client: AsyncClient,
):
    """
    Тест ручки для обновления блюда.
    Обновление описания(description).
    :return:
    """
    menu_id: str = menu_data['id']
    submenu_id: str = submenu_data['id']
    dish_id: str = dish_data['id']

    updated_description: dict[str, str] = {
        'description': 'updated description of dish'
    }

    response = await client.patch(
        reverse(
            app,
            'update_dish',
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id
        ),
        json=updated_description,
    )

    assert response.status_code == status.HTTP_200_OK
    response_data: dict[str, str] = response.json()

    assert response_data['id'] == dish_data['id']
    assert response_data['title'] == dish_data['title']
    assert response_data['description'] == updated_description['description']
    assert response_data['price'] == dish_data['price']

    dish_data['description'] = updated_description['description']


@pytest.mark.asyncio
async def test_update_price_of_dish(
        client: AsyncClient,
):
    """
    Тест ручки для обновления блюда.
    Обновление цены(price).
    :return:
    """
    menu_id: str = menu_data['id']
    submenu_id: str = submenu_data['id']
    dish_id: str = dish_data['id']

    updated_price: dict[str, str] = {
        'price': '15.30'
    }

    response = await client.patch(
        reverse(
            app,
            'update_dish',
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id
        ),
        json=updated_price,
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert response_data['id'] == dish_data['id']
    assert response_data['title'] == dish_data['title']
    assert response_data['description'] == dish_data['description']
    assert response_data['price'] == updated_price['price']

    dish_data['price'] = updated_price['price']


@pytest.mark.asyncio
async def test_update_dish(
        client: AsyncClient,
):
    """
    Тест ручки для обновления блюда.
    Обновление всех полей: название(title), описания(description), цена(price).
    :return:
    """
    menu_id: str = menu_data['id']
    submenu_id: str = submenu_data['id']
    dish_id: str = dish_data['id']

    updated_dish: dict[str, str] = {
        'title': 'twice updated title of dish',
        'description': 'twice updated description of dish',
        'price': '98.30',
    }

    response = await client.patch(
        reverse(
            app,
            'update_dish',
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id
        ),
        json=updated_dish,
    )

    assert response.status_code == status.HTTP_200_OK
    response_data: dict[str, str] = response.json()

    assert response_data['id'] == dish_data['id']
    assert response_data['title'] == updated_dish['title']
    assert response_data['description'] == updated_dish['description']
    assert response_data['price'] == updated_dish['price']


@pytest.mark.asyncio
async def test_delete_dish(
        client: AsyncClient,
):
    """
    Тест ручки для удаления блюда.
    """
    menu_id: str = menu_data['id']
    submenu_id: str = submenu_data['id']
    dish_id: str = dish_data['id']

    response = await client.delete(
        reverse(
            app,
            'delete_dish',
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id
        ),
    )

    assert response.status_code == status.HTTP_200_OK


def teardown_module():
    """
    Удаление созданных меню и сабменю.
    :return:
    """
    menu_id: str = menu_data['id']

    sync_client.delete(
        url=reverse(app, 'delete_menu', menu_id=menu_id),
    )
