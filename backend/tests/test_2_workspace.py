from pprint import pprint

import pytest
from httpx import AsyncClient


async def test_create_workspace(ac: AsyncClient):
    user_token_data = await ac.post('/user/register', json={
        "username": "TestClient_2",
        "telegram_name": "string",
        "email": "test_2@example.com",
        "role": "owner",
        "password": "12345"
    })

    user_token = user_token_data.json().get('access_token')

    response = await ac.post(
        '/workspace/',
        headers={
            'Authorization': f'JWT {user_token}'
        },
        json={
            "title": "TestWorkSpace",
        }
    )
    assert response.status_code == 201
    assert response.json().get('users') == [2]


async def test_get_workspace(ac: AsyncClient):
    response_0 = await ac.post('/user/login', json={
        'email': 'test_2@example.com',
        'password': '12345'
    })
    user_token = response_0.json().get('access_token')

    response = await ac.get(
        '/workspace/3',
        headers={
            'Authorization': f'JWT {user_token}'
        },
    )
    assert response.status_code == 200
    assert response.json().get('users') == [2]


async def test_get_workspace_unauthorized(ac: AsyncClient):
    response = await ac.get(
        '/workspace/3',
        headers={
            'Authorization': f'JWT sdfdsfsdf.sdfsdfdsfdsf.sdferwrhntbb'
        },
    )

    assert response.status_code == 401
    assert response.content.decode() == 'Unauthorized'


async def test_update_workspace(ac: AsyncClient):
    response_0 = await ac.post('/user/login', json={
        'email': 'test_2@example.com',
        'password': '12345'
    })
    user_token = response_0.json().get('access_token')

    response = await ac.patch(
        '/workspace/3',
        headers={
            'Authorization': f'JWT {user_token}'
        },
        json={
            "new_title": "New title TestWorkSpace",
        }
    )
    assert response.status_code == 200

    response = await ac.get(
        '/workspace/3',
        headers={
            'Authorization': f'JWT {user_token}'
        },
    )
    assert response.status_code == 200
    assert response.json().get('users') == [2]
    assert response.json().get('title') == 'New title TestWorkSpace'


async def test_invite_user(ac: AsyncClient):
    user3_token_data = await ac.post(
        '/user/register', json={
            "username": "TestClient_3",
            "telegram_name": "string3",
            "email": "test_3@example.com",
            "role": "owner",
            "password": "12345"
        })

    user3_token = user3_token_data.json().get('access_token')
    response = await ac.post(
        'workspace/invite',
        headers={
            'Authorization': f'JWT {user3_token}'
        },
        json={
            'inviter': 'test_2@example.com',
            'workspace_id': 4
        })
    assert response.status_code == 200


async def test_invite_undefined_user(ac: AsyncClient):
    user3_token_data = await ac.post(
        '/user/login', json={
            "email": "test_3@example.com",
            "password": "12345"
        })

    user3_token = user3_token_data.json().get('access_token')
    response = await ac.post(
        'workspace/invite',
        headers={
            'Authorization': f'JWT {user3_token}'
        },
        json={
            'inviter': 'test_10@example.com',
            'workspace_id': 3
        })
    assert response.status_code == 404


async def test_get_all_invites(ac: AsyncClient):
    user2_token_data = await ac.post(
        '/user/login', json={
            "email": "test_2@example.com",
            "password": "12345"
        })

    user2_token = user2_token_data.json().get('access_token')

    response = await ac.get(
        url='/workspace/invite',
        headers={
            'Authorization': f'JWT {user2_token}'
        },
    )

    assert response.status_code == 200


async def test_resolve_invite(ac: AsyncClient):
    user2_token_data = await ac.post(
        '/user/login', json={
            "email": "test_2@example.com",
            "password": "12345"
        })

    user2_token = user2_token_data.json().get('access_token')

    response = await ac.patch(
        '/workspace/invite',
        headers={
            'Authorization': f'JWT {user2_token}'
        },
        json={
            'id': 1,
            'result': True
        }
    )

    assert response.status_code == 200

    response_get_workspace = await ac.get(
        url='workspace/all',
        headers={
            'Authorization': f'JWT {user2_token}'
        },
    )

    assert response_get_workspace.status_code == 200


async def test_get_all_workspaces(ac: AsyncClient):
    user2_token_data = await ac.post(
        '/user/login', json={
            "email": "test_2@example.com",
            "password": "12345"
        })

    user2_token = user2_token_data.json().get('access_token')

    response = await ac.get(
        url='/workspace/all',
        headers={
            'Authorization': f'JWT {user2_token}'
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_users_in_workspace(ac: AsyncClient):
    user2_token_data = await ac.post(
        '/user/login', json={
            "email": "test_2@example.com",
            "password": "12345"
        })

    user2_token = user2_token_data.json().get('access_token')

    response = await ac.get(
        url='/workspace/4/users',
        headers={
            'Authorization': f'JWT {user2_token}'
        },
    )

    assert response.status_code == 200
    result = response.json()
    assert len(result) == 2
    # pprint(result)


async def test_get_users_in_foreign_workspace(ac: AsyncClient):
    user2_token_data = await ac.post(
        '/user/login', json={
            "email": "test_2@example.com",
            "password": "12345"
        })

    user2_token = user2_token_data.json().get('access_token')

    response = await ac.get(
        url='/workspace/1/users',
        headers={
            'Authorization': f'JWT {user2_token}'
        },
    )

    assert response.status_code == 404
    assert response.content.decode() == 'User not in workspace'

# async def test_add_workspace(ac: AsyncClient):
#     response_0 = await ac.post('/user/login', json={
#         'email': 'test_2@example.com',
#         'password': '12345'
#     })
#     access_token = response_0.json().get('access_token')
#
#     response = await ac.patch(
#         '/2',
#         headers={
#             'Authorization': f'JWT {access_token}'
#         },
#         json={
#             'workspace': 'TestWorkSpace',
#             'new_name': 'Second test workspace',
#         }
#     )
#     workspace = response.json()
#     assert response.status_code == 200
#     assert isinstance(workspace.id, int)
#     assert workspace.title == 'Second test workspace'
#     assert workspace.users == [2]
# id: int
# title: str
# users: List
#
# async def test_update_workspace(ac: AsyncClient):
#     response = await ac.patch(
#         '/workspace/update',
#         headers={
#             'Authorize': 'JWT 12345'
#         },
#         json={
#             'id': 1,
#             'title': 'New name workspace',
#         }
#     )
#     assert response.status_code == 200
#
#
# async def test_get_workspace(ac: AsyncClient):
#     response = await ac.get(
#         '/workspace/1',
#         headers={
#             'Authorization': 'JWT 12345'
#         }
#     )
#     workspace = response.json()
#     assert response.status_code == 200
#     assert workspace.get('id') == 1
#     assert workspace.get('title') == 'New name workspace'
#
