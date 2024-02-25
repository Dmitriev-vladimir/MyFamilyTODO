import pytest
from httpx import AsyncClient


async def test_create_project(ac: AsyncClient):
    user_token_data = await ac.post('/user/register', json={
        "username": "TestClientProject_2",
        "telegram_name": "string",
        "email": "test_2_project@example.com",
        "role": "owner",
        "password": "12345"
    })

    user_token = user_token_data.json().get('access_token')

    response = await ac.post(
        'project/',
        headers={
            'Authorization': f'JWT {user_token}'
        },
        json={
            'title': 'Test Project',
            'workspace_id': 5
        })
    assert response.status_code == 201


async def test_update_project_by_title(ac: AsyncClient):
    user_token_data = await ac.post('/user/login', json={
        "email": "test_2_project@example.com",
        "password": "12345"
    })

    user_token = user_token_data.json().get('access_token')

    workspace_response = await ac.post(
        url='/workspace/',
        headers={
            'Authorization': f'JWT {user_token}'
        },
        json={
            'title': 'Second test workspace for project'
        }
    )

    response = await ac.post(
        url='/project/1',
        headers={
            'Authorization': f'JWT {user_token}'
        },
        json={
            'title': 'New Test Project',
        }
    )

    assert response.status_code == 200


async def test_update_project_by_workspace(ac: AsyncClient):
    user_token_data = await ac.post('/user/login', json={
        "email": "test_2_project@example.com",
        "password": "12345"
    })

    user_token = user_token_data.json().get('access_token')

    response = await ac.post(
        url='/project/1',
        headers={
            'Authorization': f'JWT {user_token}'
        },
        json={
            'workspace_id': 6
        }
    )

    assert response.status_code == 200


async def test_get_projects_in_workspace(ac: AsyncClient):
    user_token_data = await ac.post('/user/login', json={
        "email": "test_2_project@example.com",
        "password": "12345"
    })

    user_token = user_token_data.json().get('access_token')

    response = await ac.get(
        url='/project/6/all',
        headers={
            'Authorization': f'JWT {user_token}'
        },
    )

    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1
