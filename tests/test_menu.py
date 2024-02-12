import pytest
from httpx import AsyncClient
from starlette import status

from main import app
from src.core.utils import reverse

menu_data: dict[str, str] = {
    'title': 'menu 1',
    'description': 'description of menu 1',
}


@pytest.mark.asyncio
async def test_get_all_menus(
        client: AsyncClient,
):
    """
    Тест ручки для получения всех меню.
    :return:
    """
    response = await client.get(
        url=reverse(app, 'get_all_menus'),
    )

    assert response.status_code == status.HTTP_200_OK

    response_data: list[dict[str, str]] = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 0


@pytest.mark.asyncio
async def test_add_menus(
        client: AsyncClient,
):
    """
    Тест ручки для создания меню.
    :return:
    """
    response = await client.post(
        reverse(app, 'create_menu'),
        json=menu_data,
    )
    assert response.status_code == status.HTTP_201_CREATED

    response_data: dict[str, str] = response.json()
    assert response_data.get('id')
    assert response_data.get('title')
    assert response_data.get('description')

    assert response_data['title'] == menu_data['title']
    assert response_data['description'] == menu_data['description']

    response = await client.get(
        reverse(app, 'get_all_menus')
    )
    assert response.status_code == status.HTTP_200_OK

    get_all_response_data: list[dict[str, str]] = response.json()
    assert isinstance(get_all_response_data, list)
    assert len(get_all_response_data) == 1

    menu_data['id'] = response_data['id']


@pytest.mark.asyncio
async def test_get_menu(
        client: AsyncClient,
):
    """
    Тест ручки для получения конкретного меню.
    :return:
    """
    menu_id: str = menu_data['id']
    response = await client.get(
        reverse(app, 'get_menu_by_id', menu_id=menu_id)
    )
    assert response.status_code == status.HTTP_200_OK

    response_data: dict[str, str] = response.json()
    assert response_data.get('id')
    assert response_data.get('title')
    assert response_data.get('description')

    assert response_data['title'] == menu_data['title']
    assert response_data['description'] == menu_data['description']


@pytest.mark.asyncio
async def test_update_title_of_menu(
        client: AsyncClient,
):
    """
    Тест ручки для обновления меню.
    Обновления названия(title).
    :return:
    """
    updated_title: dict[str, str] = {
        'title': 'update menu 1'
    }

    menu_id: str = menu_data['id']
    response = await client.patch(
        reverse(app, 'update_menu', menu_id=menu_id),
        json=updated_title,
    )
    assert response.status_code == status.HTTP_200_OK
    response_data: dict[str, str] = response.json()

    assert response_data['title'] == updated_title['title']
    assert response_data['description'] == menu_data['description']

    menu_data['title'] = updated_title['title']


@pytest.mark.asyncio
async def test_update_description_of_menu(
        client: AsyncClient,
):
    """
    Тест ручки для обновления меню.
    Обновления описания(description).
    :return:
    """
    updated_description = {
        'description': 'updated description of menu 1'
    }

    menu_id: str = menu_data['id']
    response = await client.patch(
        reverse(app, 'update_menu', menu_id=menu_id),
        json=updated_description,
    )
    assert response.status_code == status.HTTP_200_OK
    response_data: dict[str, str] = response.json()

    assert response_data['title'] == menu_data['title']
    assert response_data['description'] == updated_description['description']

    menu_data['description'] = updated_description['description']


@pytest.mark.asyncio
async def test_update_menu(
        client: AsyncClient,
):
    """
    Тест ручки для обновления меню.
    Обновление названия(title) и описания(description).
    :return:
    """
    updated_menu = {
        'title': 'twice updated of menu 1',
        'description': 'twice updated description of menu 1',
    }

    menu_id: str = menu_data['id']
    response = await client.patch(
        reverse(app, 'update_menu', menu_id=menu_id),
        json=updated_menu,
    )

    assert response.status_code == status.HTTP_200_OK

    response_data: dict[str, str] = response.json()
    assert response_data.get('id')
    assert response_data.get('title')
    assert response_data.get('description')

    assert response_data['title'] == updated_menu['title']
    assert response_data['description'] == updated_menu['description']

    menu_data['title'] = updated_menu['title']
    menu_data['description'] = updated_menu['description']


@pytest.mark.asyncio
async def test_delete_menu(
        client: AsyncClient,
):
    """
    Тест ручки для удаления меню.
    :return:
    """
    menu_id: str = menu_data['id']
    response = await client.delete(
        reverse(app, 'delete_menu', menu_id=menu_id),
    )
    assert response.status_code == status.HTTP_200_OK

    response = await client.get(
        reverse(app, 'get_menu_by_id', menu_id=menu_id)
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = await client.get(
        url=reverse(app, 'get_all_menus'),
    )
    assert response.status_code == status.HTTP_200_OK
    response_data: dict[str, str] = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 0
