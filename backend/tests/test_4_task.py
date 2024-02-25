import pytest
from httpx import AsyncClient


async def test_create_task(ac: AsyncClient):
    user_token_data = await ac.post('/user/login', json={
        "email": "test_2@example.com",
        "password": "12345"
    })

    user_token = user_token_data.json().get('access_token')

    response = await ac.post(
        '/task/',
        headers={
            'Authorization': f'JWT {user_token}'
        },
        json={
            'title': 'First test task',
            'project_id': 1,
        }
    )

    result = response.json()

    assert response.status_code == 201
    assert result.get('id') == 1
    assert result.get('title') == 'First test task'
    assert result.get('executor') is None


async def test_update_task_incorrect_status(ac: AsyncClient):
    user_token_data = await ac.post('/user/login', json={
        "email": "test_2@example.com",
        "password": "12345"
    })

    user_token = user_token_data.json().get('access_token')

    response = await ac.patch(
        '/task/',
        headers={
            'Authorization': f'JWT {user_token}'
        },
        json={
            'id': 1,
            'title': 'New First test task',
            'executor': 3,
            'status': 'some'
        }
    )

    # result = response.json()

    assert response.status_code == 422
    # assert result.get('id') == 1
    # assert result.get('title') == 'New First test task'
    # assert result.get('executor') == 3


async def test_update_task(ac: AsyncClient):
    user_token_data = await ac.post('/user/login', json={
        "email": "test_2@example.com",
        "password": "12345"
    })

    user_token = user_token_data.json().get('access_token')

    response = await ac.patch(
        '/task/',
        headers={
            'Authorization': f'JWT {user_token}'
        },
        json={
            'id': 1,
            'title': 'New First test task',
            'executor': 3,
            'status': 'done'
        }
    )

    result = response.json()

    assert response.status_code == 200
    assert result.get('id') == 1
    assert result.get('title') == 'New First test task'
    assert result.get('executor') == 3


async def test_create_color(ac: AsyncClient):
    user_token_data = await ac.post('/user/login', json={
        "email": "test_2@example.com",
        "password": "12345"
    })

    user_token = user_token_data.json().get('access_token')
    response = await ac.post(
        '/color/',
        headers={
            'Authorization': f'JWT {user_token}'
        },
        json={
            'name': 'black',
            'value': '#000000',
            'workspace_id': 3
        }
    )

    assert response.status_code == 201

    result = response.json()
    assert result.get('id') == 1
    assert result.get('name') == 'black'


async def test_get_color(ac: AsyncClient):
    user_token_data = await ac.post('/user/login', json={
        "email": "test_2@example.com",
        "password": "12345"
    })

    user_token = user_token_data.json().get('access_token')
    response = await ac.get(
        '/color/1',
        headers={
            'Authorization': f'JWT {user_token}'
        },
    )

    assert response.status_code == 200

    result = response.json()
    assert result.get('id') == 1
    assert result.get('name') == 'black'


async def test_get_all_colors(ac: AsyncClient):
    user_token_data = await ac.post('/user/login', json={
        "email": "test_2@example.com",
        "password": "12345"
    })

    user_token = user_token_data.json().get('access_token')

    response = await ac.get(
        url='/color/all/3',
        headers={
            'Authorization': f'JWT {user_token}'
        },
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_all_colors_in_foreign_workspace(ac: AsyncClient):
    user_token_data = await ac.post('/user/login', json={
        "email": "test_2@example.com",
        "password": "12345"
    })

    user_token = user_token_data.json().get('access_token')

    response = await ac.get(
        url='/color/all/1',
        headers={
            'Authorization': f'JWT {user_token}'
        },
    )

    assert response.status_code == 404
    assert response.content.decode() == 'Not valid workspace'


async def test_update_color(ac: AsyncClient):
    user_token_data = await ac.post('/user/login', json={
        "email": "test_2@example.com",
        "password": "12345"
    })

    user_token = user_token_data.json().get('access_token')

    response = await ac.patch(
        url='/color/',
        headers={
            'Authorization': f'JWT {user_token}'
        },
        json={
            'id': 1,
            'name': 'new color'
        }
    )

    assert response.status_code == 200


async def test_update_color_by_invalid_workspace(ac: AsyncClient):
    user_token_data = await ac.post('/user/login', json={
        "email": "test@example.com",
        "password": "12345"
    })

    user_token = user_token_data.json().get('access_token')

    response = await ac.patch(
        url='/color/',
        headers={
            'Authorization': f'JWT {user_token}'
        },
        json={
            'id': 1,
            'name': 'new color'
        }
    )

    assert response.status_code == 404
    assert response.content.decode() == 'User not in color workspace'


async def test_create_tag(ac: AsyncClient):
    user_token_data = await ac.post('/user/login', json={
        "email": "test_2@example.com",
        "password": "12345"
    })

    user_token = user_token_data.json().get('access_token')

    response = await ac.post(
        url='/tag/',
        headers={
            'Authorization': f'JWT {user_token}'
        },
        json={
            'name': 'first tag',
            'workspace_id': 2
        }
    )

    assert response.status_code == 201
    assert response.json().get('name') == 'first tag'


async def test_update_tag_name(ac: AsyncClient):
    user_token_data = await ac.post('/user/login', json={
        "email": "test_2@example.com",
        "password": "12345"
    })

    user_token = user_token_data.json().get('access_token')

    response = await ac.patch(
        url='/tag/',
        headers={
            'Authorization': f'JWT {user_token}'
        },
        json={
            'id': 1,
            'name': 'new tag name',
        }
    )

    assert response.status_code == 200
    assert response.json().get('name') == 'new tag name'


async def test_update_tag_name_invalid_user(ac: AsyncClient):
    user_token_data = await ac.post('/user/login', json={
        "email": "test@example.com",
        "password": "12345"
    })

    user_token = user_token_data.json().get('access_token')

    response = await ac.patch(
        url='/tag/',
        headers={
            'Authorization': f'JWT {user_token}'
        },
        json={
            'id': 1,
            'name': 'test tag name',
        }
    )

    assert response.status_code == 404


async def test_get_all_tags(ac: AsyncClient):
    user_token_data = await ac.post('/user/login', json={
        "email": "test_2@example.com",
        "password": "12345"
    })

    user_token = user_token_data.json().get('access_token')

    response = await ac.get(
        url='/tag/all/2',
        headers={
            'Authorization': f'JWT {user_token}'
        },
    )

    assert response.status_code == 200
    tags_list = response.json()
    assert isinstance(tags_list, list)
    assert len(tags_list) == 1
    assert tags_list[0].get('name') == 'new tag name'


async def test_get_all_tags_in_foreign_workspace(ac: AsyncClient):
    user_token_data = await ac.post('/user/login', json={
        "email": "test_2@example.com",
        "password": "12345"
    })

    user_token = user_token_data.json().get('access_token')

    response = await ac.get(
        url='/tag/all/1',
        headers={
            'Authorization': f'JWT {user_token}'
        },
    )

    assert response.status_code == 404


async def test_get_all_tasks_in_project(ac: AsyncClient):
    user_token_data = await ac.post('/user/login', json={
        "email": "test_2_project@example.com",
        "password": "12345"
    })

    user_token = user_token_data.json().get('access_token')

    response = await ac.get(
        url='/task/project/1/all',
        headers={
            'Authorization': f'JWT {user_token}'
        },
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_all_tasks_in_workspace(ac: AsyncClient):
    user_token_data = await ac.post('/user/login', json={
        "email": "test_2@example.com",
        "password": "12345"
    })

    user_token = user_token_data.json().get('access_token')

    response = await ac.get(
        url='/task/workspace/4/all',
        headers={
            'Authorization': f'JWT {user_token}'
        },
    )
    assert response.status_code == 200
    assert len(response.json()) == 0
