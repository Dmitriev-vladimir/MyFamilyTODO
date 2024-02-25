from time import sleep

import pytest
from httpx import AsyncClient


async def test_register(ac: AsyncClient):
    response = await ac.post('/user/register', json={
        "username": "TestClient",
        "telegram_name": "string",
        "email": "test@example.com",
        "role": "owner",
        "password": "12345"
    })
    assert response.status_code == 201
    assert isinstance(response.json().get('access_token'), str)


async def test_login(ac: AsyncClient):
    response = await ac.post('/user/login', json={
        'email': 'test@example.com',
        'password': '12345'
    })

    assert response.status_code == 200
    assert isinstance(response.json().get('access_token'), str)


async def test_incorrect_password(ac: AsyncClient):
    response = await ac.post('/user/login', json={
        'email': 'test@example.com',
        'password': '1234'
    })
    assert response.status_code == 401
    assert response.content.decode() == 'Unauthorized'


async def test_unknown_user_login(ac: AsyncClient):
    response = await ac.post('user/login', json={
        'email': 'qwerty@main.com',
        'password': '12345'
    })
    assert response.status_code == 401
    assert response.content.decode() == 'User does not exist'


async def test_get_all_users(ac: AsyncClient):
    response_0 = await ac.post('/user/login', json={
        'email': 'test@example.com',
        'password': '12345'
    })
    access_token = response_0.json().get('access_token')

    response = await ac.get('/user/all/1', headers={
        'Authorization': f'JWT {access_token}'
    })
    assert response.status_code == 200
    assert len(response.json()) == 1
    result = response.json()
    assert result[0].get('id') == 1
    assert result[0].get('username') == 'TestClient'
    assert result[0].get('role') == 'owner'


async def test_get_self_user(ac: AsyncClient):
    response_0 = await ac.post('/user/login', json={
        'email': 'test@example.com',
        'password': '12345'
    })
    access_token = response_0.json().get('access_token')
    sleep(2)
    second_response = await ac.post('/token/refresh', json={
        'refresh_token': response_0.json().get('refresh_token')
    })
    response = await ac.get('/user/self', headers={
        'Authorization': f'JWT {second_response.json().get("access_token")}'
    })
    assert response.status_code == 200
    user = response.json()
    assert user.get('id') == 1
    assert user.get('email') == 'test@example.com'
    assert user.get('username') == 'TestClient'


async def test_update_user(ac: AsyncClient):
    response_0 = await ac.post('/user/login', json={
        'email': 'test@example.com',
        'password': '12345'
    })
    access_token = response_0.json().get('access_token')

    response = await ac.patch(
        '/user/self',
        headers={
            'Authorization': f'JWT {access_token}'
        },
        json={
            'username': 'New Client Name',
        }
    )
    assert response.status_code == 200

    response_user = await ac.get('/user/self', headers={
        'Authorization': f'JWT {access_token}'
    })
    user = response_user.json()
    assert user.get('username') == 'New Client Name'
    assert user.get('email') == 'test@example.com'
    assert user.get('telegram_name') == 'string'


def test_get_user_by_tlg_name(ac: AsyncClient):
    ...


async def test_delete_user(ac: AsyncClient):
    response_0 = await ac.post('/user/login', json={
        'email': 'test@example.com',
        'password': '12345'
    })
    access_token = response_0.json().get('access_token')

    response = await ac.delete('/user/self', headers={
        'Authorization': f'JWT {access_token}'
    })

    assert response.status_code == 204

    response_2 = await ac.get('/user/self', headers={
        'Authorization': f'JWT {access_token}'
    })
    user = response_2.json()
    assert response_2.status_code == 200
    # assert len(users) == 1
    assert user.get('is_active') is False
