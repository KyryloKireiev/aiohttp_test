import json

import pytest

from blog.utils import check_hash, generate_hash


@pytest.mark.asyncio
async def test_index_view(test_client):
    resp = await test_client.get("/")
    assert resp.status == 200


@pytest.mark.asyncio
async def test_users_view(test_client):
    resp = await test_client.get("/users/")
    assert resp.status == 200


@pytest.mark.asyncio
async def test_user_sign_up(test_client):
    valid_user = {"username": "user", "password": "password"}

    exist_user = valid_user

    invalid_username = {"username": "u", "password": "password"}

    invalid_password = {"username": "user123", "password": "1234"}

    unknown_field = {"user": "user_2", "password": "password"}

    extra_field = {"username": "user_3", "password": "password", "age": 123}

    resp = await test_client.post("/sign-up/", json=valid_user)
    user = await test_client.get("/users/")
    result = json.loads(await user.read())
    assert user.status == 200
    assert resp.status == 201
    assert result["users"][0]["username"] == "user"
    assert result["users"][0]["id"] == 1
    assert result["count"] == 1

    resp = await test_client.post("/sign-up/", json=exist_user)
    assert resp.status == 409
    result = json.loads(await resp.read())
    assert result["message"] == "user with the same name already exists"

    resp = await test_client.post("/sign-up/", json=invalid_username)
    assert resp.status == 409
    result = await resp.read()
    result = result.decode("utf-8")
    assert result == "{'username': ['Length must be between 3 and 50.']}"

    resp = await test_client.post("/sign-up/", json=invalid_password)
    assert resp.status == 409
    result = await resp.read()
    result = result.decode("utf-8")
    assert result == "{'password': ['Length must be between 8 and 25.']}"

    resp = await test_client.post("/sign-up/", json=unknown_field)
    assert resp.status == 409

    resp = await test_client.post("/sign-up/", json=extra_field)
    assert resp.status == 409


def test_security():
    user_password = "password"
    wrong_password = "12345678"

    hashed = generate_hash(user_password)
    assert check_hash(user_password, hashed)
    assert not check_hash(wrong_password, hashed)
