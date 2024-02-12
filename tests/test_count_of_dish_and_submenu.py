import pytest
from httpx import AsyncClient
from starlette import status

from main import app
from src.core.utils import reverse

menu_data = {
    'title': 'menu',
    'description': 'description of menu',
}

submenu_data = {
    'title': 'submenu',
    'description': 'description of submenu',
}


@pytest.mark.asyncio
async def test_create_menu_for_counting_test(
        client: AsyncClient,
):
    """
    :return:
    """
    response = await client.post(
        reverse(app, 'create_menu'),
        json=menu_data,
    )
    assert response.status_code == status.HTTP_201_CREATED

    created_menu: dict[str, str] = response.json()

    assert 'id' in created_menu.keys()
    assert 'title' in created_menu.keys()
    assert 'description' in created_menu.keys()
    assert 'submenus_count' in created_menu.keys()
    assert 'dishes_count' in created_menu.keys()

    assert created_menu['submenus_count'] == 0
    assert created_menu['dishes_count'] == 0

    menu_data['id'] = created_menu['id']


@pytest.mark.asyncio
async def test_create_submenu_for_counting_test(
        client: AsyncClient,
):
    """
    :return:
    """
    menu_id: str = menu_data['id']

    response = await client.post(
        reverse(app, 'create_submenu', menu_id=menu_id),
        json=submenu_data,
    )
    assert response.status_code == status.HTTP_201_CREATED

    submenu_data['id'] = response.json()['id']


@pytest.mark.asyncio
async def test_create_dish1_for_counting_test(
        client: AsyncClient,
):
    """
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
        json={
            'price': '12.45',
            'title': 'dish 1',
            'description': 'description of dish 1',
        },
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_create_dish2_for_counting_test(
        client: AsyncClient,
):
    """
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
        json={
            'price': '12.56',
            'title': 'dish 2',
            'description': 'description of dish 2',
        },
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_check_menu(
        client: AsyncClient,
):
    """
    :return:
    """
    menu_id: str = menu_data['id']
    response = await client.get(
        reverse(app, 'get_menu_by_id', menu_id=menu_id)
    )

    assert response.status_code == status.HTTP_200_OK

    response_data: dict[str, str] = response.json()

    assert 'id' in response_data.keys()
    assert 'submenus_count' in response_data.keys()
    assert 'dishes_count' in response_data.keys()

    assert response_data['submenus_count'] == 1
    assert response_data['dishes_count'] == 2


@pytest.mark.asyncio
async def test_check_submenu(
        client: AsyncClient,
):
    """
    :return:
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

    assert 'id' in response_data.keys()
    assert 'dishes_count' in response_data.keys()

    assert response_data['dishes_count'] == 2


@pytest.mark.asyncio
async def test_delete_submenu(
        client: AsyncClient,
):
    """
    :return:
    """
    menu_id: str = menu_data['id']
    submenu_id: str = submenu_data['id']

    response = await client.delete(
        reverse(
            app,
            'delete_submenu',
            menu_id=menu_id,
            submenu_id=submenu_id
        )
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def get_all_submenus(
        client: AsyncClient,
):
    """
    :return:
    """
    menu_id: str = menu_data['id']
    response = await client.get(
        reverse(
            app,
            'get_all_submenus',
            menu_id=menu_id,
        )
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() is []


@pytest.mark.asyncio
async def test_get_all_dishes(
        client: AsyncClient,
):
    """
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
    response_data: list[dict[str, str]] = response.json()
    assert len(response_data) == 0


@pytest.mark.asyncio
async def test_check_menu_2(
        client: AsyncClient,
):
    """
    :return:
    """
    menu_id: str = menu_data['id']
    response = await client.get(
        reverse(app, 'get_menu_by_id', menu_id=menu_id),
    )

    assert response.status_code == status.HTTP_200_OK

    response_data: dict[str, str] = response.json()

    assert 'id' in response_data.keys()
    assert 'submenus_count' in response_data.keys()
    assert 'dishes_count' in response_data.keys()

    assert response_data['submenus_count'] == 0
    assert response_data['dishes_count'] == 0


@pytest.mark.asyncio
async def test_delete_menu(
        client: AsyncClient,
):
    """
    :return:
    """
    menu_id: str = menu_data['id']
    response = await client.delete(
        reverse(app, 'delete_menu', menu_id=menu_id),
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_all_menus(
        client: AsyncClient,
):
    """
    :return:
    """
    response = await client.get(
        reverse(app, 'get_all_menus'),
    )

    assert response.status_code == status.HTTP_200_OK
    response_data: list[dict[str, str]] = response.json()
    assert len(response_data) == 0
