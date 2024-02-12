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

dish1_data = {
    'title': 'dish1',
    'description': 'description of dish1',
    'price': '12.45'
}

dish2_data = {
    'title': 'dish2',
    'description': 'description of dish2',
    'price': '1.34'
}


@pytest.mark.asyncio
async def test_full_base_start(
        client: AsyncClient,
):
    """Проверка, что на начало тестов, база пуста."""
    response = await client.get(
        url=reverse(app, 'full_base'),
    )

    assert response.status_code == status.HTTP_200_OK

    response_data: list[dict[str, str]] = response.json()
    assert response_data == []


@pytest.mark.asyncio
async def test_create_menu(
        client: AsyncClient,
):
    """Создание меню"""
    response = await client.post(
        url=reverse(app, 'create_menu'),
        json=menu_data,
    )

    assert response.status_code == status.HTTP_201_CREATED

    menu_data['id'] = response.json()['id']


@pytest.mark.asyncio
async def test_full_base_1(
        client: AsyncClient,
):
    """
    Проверка, что endpoint со всей базой выдаёт созданное меню.
    Проверка, что список подменю - пуст.
    """
    response = await client.get(
        url=reverse(app, 'full_base'),
    )

    assert response.status_code == status.HTTP_200_OK

    response_data: list[dict[str, str]] = response.json()
    assert len(response_data) == 1

    assert response_data[0]['submenus'] == []


@pytest.mark.asyncio
async def test_create_submenu(
        client: AsyncClient
):
    """Создание подменю"""
    response = await client.post(
        url=reverse(app, 'create_submenu', menu_id=menu_data['id']),
        json=submenu_data,
    )

    assert response.status_code == status.HTTP_201_CREATED

    submenu_data['id'] = response.json()['id']


@pytest.mark.asyncio
async def test_full_base_2(
        client: AsyncClient,
):
    """
    Проверка, что endpoint со всей базой выдаёт созданное меню и связанное подменю.
    Проверка, что список блюд у подменю - пуст.
    """
    response = await client.get(
        url=reverse(app, 'full_base'),
    )

    assert response.status_code == status.HTTP_200_OK

    response_data: list[dict[str, str]] = response.json()
    assert len(response_data) == 1

    menu = response_data[0]

    assert menu['id'] == menu_data['id']

    assert len(menu['submenus']) == 1


@pytest.mark.asyncio
async def test_create_dishes(
        client: AsyncClient
):
    """Создание 2-х блюд"""
    response = await client.post(
        url=reverse(
            app,
            'create_dish',
            menu_id=menu_data['id'],
            submenu_id=submenu_data['id'],
        ),
        json=dish1_data,
    )

    assert response.status_code == status.HTTP_201_CREATED

    dish1_data['id'] = response.json()['id']

    response = await client.post(
        url=reverse(
            app,
            'create_dish',
            menu_id=menu_data['id'],
            submenu_id=submenu_data['id'],
        ),
        json=dish2_data,
    )

    assert response.status_code == status.HTTP_201_CREATED

    dish1_data['id'] = response.json()['id']


@pytest.mark.asyncio
async def test_full_base_3(
        client: AsyncClient,
):
    """
    Проверка, что endpoint со всей базой выдаёт созданное меню и
    связанное подменю со связанными блюдами.
    """
    response = await client.get(
        url=reverse(app, 'full_base'),
    )

    assert response.status_code == status.HTTP_200_OK

    response_data: list[dict] = response.json()
    assert len(response_data) == 1

    menu = response_data[0]

    assert menu['id'] == menu_data['id']

    assert len(menu['submenus']) == 1

    submenu = menu['submenus'][0]
    assert submenu['id'] == submenu_data['id']

    assert len(submenu['dishes']) == 2


@pytest.mark.asyncio
async def test_delete_dish(
        client: AsyncClient,
):
    """Удалить блюдо"""
    response = await client.delete(
        url=reverse(
            app,
            'delete_dish',
            menu_id=menu_data['id'],
            submenu_id=submenu_data['id'],
            dish_id=dish1_data['id'],
        )
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_full_base_4(
        client: AsyncClient,
):
    """
    Проверка, что endpoint со всей базой выдаёт созданное меню и
    связанное подменю со связанными блюдами.
    После удаления блюда, количество блюд должно уменьшиться на 1
    """
    response = await client.get(
        url=reverse(app, 'full_base'),
    )

    assert response.status_code == status.HTTP_200_OK

    response_data: list[dict] = response.json()
    assert len(response_data) == 1

    menu = response_data[0]

    assert menu['id'] == menu_data['id']
    assert len(menu['submenus']) == 1

    submenu = menu['submenus'][0]
    assert submenu['id'] == submenu_data['id']
    assert len(submenu['dishes']) == 1


@pytest.mark.asyncio
async def test_delete_submenu(
        client: AsyncClient,
):
    """Удаление подменю"""
    response = await client.delete(
        url=reverse(
            app,
            'delete_submenu',
            menu_id=menu_data['id'],
            submenu_id=submenu_data['id'],
        )
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_full_base_5(
        client: AsyncClient,
):
    """Проверка, что в базе осталось только одно меню, без подменю."""
    response = await client.get(
        url=reverse(app, 'full_base'),
    )

    assert response.status_code == status.HTTP_200_OK

    response_data: list[dict] = response.json()
    assert len(response_data) == 1

    menu = response_data[0]

    assert menu['id'] == menu_data['id']
    assert len(menu['submenus']) == 0


@pytest.mark.asyncio
async def test_delete_menu(
        client: AsyncClient,
):
    """Удалить меню"""
    response = await client.delete(
        url=reverse(
            app,
            'delete_menu',
            menu_id=menu_data['id'],
        )
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_full_base_final(
        client: AsyncClient,
):
    """База пуста"""
    response = await client.get(
        url=reverse(app, 'full_base'),
    )

    assert response.status_code == status.HTTP_200_OK

    response_data: list[dict] = response.json()
    assert response_data == []
