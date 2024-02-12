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


def setup_module():
    """
    Создание меню, к которому будет принадлежать сабменю.
    :return:
    """
    response = sync_client.post(
        reverse(app, 'create_menu'),
        json=menu_data,
    )

    menu_data['id'] = response.json()['id']


@pytest.mark.asyncio
async def test_get_all_submenus(
        client: AsyncClient,
):
    """
    Тест ручки для получения всех сабменю.
    :return:
    """
    menu_id: str = menu_data['id']
    response = await client.get(
        reverse(app, 'get_all_submenus', menu_id=menu_id),
    )

    assert response.status_code == status.HTTP_200_OK
    response_data: list[dict[str, str]] = response.json()

    assert isinstance(response_data, list)
    assert len(response_data) == 0


@pytest.mark.asyncio
async def test_create_submenu(
        client: AsyncClient,
):
    """
    Тест ручки для создания сабменю.
    """
    menu_id: str = menu_data['id']
    response = await client.post(
        reverse(app, 'create_submenu', menu_id=menu_id),
        json=submenu_data
    )

    assert response.status_code == status.HTTP_201_CREATED
    response_data: dict[str, str] = response.json()

    assert response_data.get('id')
    assert response_data.get('title')
    assert response_data.get('description')

    assert response_data['title'] == submenu_data['title']
    assert response_data['description'] == submenu_data['description']

    submenu_id: str = response_data['id']
    submenu_data['id'] = submenu_id


@pytest.mark.asyncio
async def test_get_submenu(
        client: AsyncClient,
):
    """
    Тест ручки для получения сабменю.
    """
    menu_id: str = menu_data['id']
    submenu_id: str = submenu_data['id']

    response = await client.get(
        reverse(
            app,
            'get_submenu',
            menu_id=menu_id,
            submenu_id=submenu_id
        ),
    )

    assert response.status_code == status.HTTP_200_OK
    response_data: dict[str, str] = response.json()

    assert response_data.get('id')
    assert response_data.get('title')
    assert response_data.get('description')

    assert response_data['id'] == submenu_data['id']
    assert response_data['title'] == submenu_data['title']
    assert response_data['description'] == submenu_data['description']


@pytest.mark.asyncio
async def test_update_title_of_submenu(
        client: AsyncClient,
):
    """
    Тест ручки для обновления сабменю.
    Обновление названия(title).
    """
    menu_id: str = menu_data['id']
    submenu_id: str = submenu_data['id']

    updated_title: dict[str, str] = {
        'title': 'updated title of submenu'
    }

    response = await client.patch(
        reverse(
            app,
            'update_submenu',
            menu_id=menu_id,
            submenu_id=submenu_id
        ),
        json=updated_title,
    )

    assert response.status_code == status.HTTP_200_OK
    response_data: dict[str, str] = response.json()

    assert response_data['id'] == submenu_data['id']
    assert response_data['title'] == updated_title['title']
    assert response_data['description'] == submenu_data['description']

    submenu_data['title'] = updated_title['title']


@pytest.mark.asyncio
async def test_update_description_of_submenu(
        client: AsyncClient,
):
    """
    Тест ручки для обновления сабменю.
    Обновление описания(description).
    """
    menu_id: str = menu_data['id']
    submenu_id: str = submenu_data['id']

    updated_description: dict[str, str] = {
        'description': 'updated description of submenu'
    }

    response = await client.patch(
        reverse(
            app,
            'update_submenu',
            menu_id=menu_id,
            submenu_id=submenu_id
        ),
        json=updated_description,
    )

    assert response.status_code == status.HTTP_200_OK
    response_data: dict[str, str] = response.json()

    assert response_data['id'] == submenu_data['id']
    assert response_data['title'] == submenu_data['title']
    assert response_data['description'] == updated_description['description']

    submenu_data['description'] = updated_description['description']


@pytest.mark.asyncio
async def test_update_submenu(
        client: AsyncClient,
):
    """
    Тест ручки для обновления сабменю.
    Обновление названия(title) и описания(desciption).
    """
    menu_id: str = menu_data['id']
    submenu_id: str = submenu_data['id']

    updated_data: dict[str, str] = {
        'title': 'twice updated title of submenu',
        'description': 'twice updated description of submenu'
    }

    response = await client.patch(
        reverse(
            app,
            'update_submenu',
            menu_id=menu_id,
            submenu_id=submenu_id
        ),
        json=updated_data,
    )

    assert response.status_code == status.HTTP_200_OK
    response_data: dict[str, str] = response.json()

    assert response_data['id'] == submenu_data['id']
    assert response_data['title'] == updated_data['title']
    assert response_data['description'] == updated_data['description']


@pytest.mark.asyncio
async def test_number_dishes(
        client: AsyncClient,
):
    menu_id: str = menu_data['id']
    submenu_id: str = submenu_data['id']

    response = await client.post(
        reverse(
            app,
            'create_dish',
            menu_id=menu_id,
            submenu_id=submenu_id
        ),
        json={
            'title': 'dish 1',
            'description': 'description of dish 1',
            'price': '12.90',
        }
    )
    assert response.status_code == status.HTTP_201_CREATED

    response = await client.post(
        reverse(
            app,
            'create_dish',
            menu_id=menu_id,
            submenu_id=submenu_id
        ),
        json={
            'title': 'dish 2',
            'description': 'description of dish 2',
            'price': '13.00',
        }
    )
    assert response.status_code == status.HTTP_201_CREATED

    response = await client.get(
        reverse(
            app,
            'get_submenu',
            menu_id=menu_id,
            submenu_id=submenu_id
        ),
    )

    response_data: dict[str, str] = response.json()

    assert 'dishes_count' in response_data.keys()

    assert response_data['dishes_count'] == 2


@pytest.mark.asyncio
async def test_delete_submenu(
        client: AsyncClient,
):
    """
    Тест ручки для удаления сабменю.
    """
    menu_id: str = menu_data['id']
    submenu_id: str = submenu_data['id']

    response = await client.delete(
        reverse(
            app,
            'delete_submenu',
            menu_id=menu_id,
            submenu_id=submenu_id
        ),
    )

    assert response.status_code == status.HTTP_200_OK


def teardown_module():
    """
    Удалить созданное меню.
    :return:
    """
    menu_id: str = menu_data['id']

    sync_client.delete(
        url=reverse(app, 'delete_menu', menu_id=menu_id),
    )
