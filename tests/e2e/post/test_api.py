import pytest


async def test_get_post_list(client):
    response = client.get("/post/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_post_by_id(client):
    post_data = {"title": "Test Post", "content": "This is a test post."}
    create_response = client.post("/post", json=post_data)
    created_post = create_response.json()
    post_id = created_post["id"]
    response = client.get(f"/post/{post_id}")
    assert response.status_code == 200
    assert response.json()["id"] == created_post["id"]


async def test_create_post(client):
    post_data = {"title": "Test Post", "content": "This is a test post."}
    response = client.post("/post", json=post_data)
    assert response.status_code == 201
    created_post = response.json()
    assert created_post["title"] == "Test Post"
    assert created_post["content"] == "This is a test post."


async def test_update_post(client):
    post_data = {"title": "Test Post", "content": "This is a test post."}
    create_response = client.post("/post/", json=post_data)
    created_post = create_response.json()

    update_data = {"title": "Updated Title", "content": "Updated content"}
    update_response = client.put(f"/post/{created_post['id']}", json=update_data)
    assert update_response.status_code == 200
    updated_post = update_response.json()
    assert updated_post["title"] == "Updated Title"


async def test_delete_post(client):
    post_data = {"title": "Test Post", "content": "This is a test post."}
    create_response = client.post("/post/", json=post_data)
    created_post = create_response.json()

    delete_response = client.delete(f"/post/{created_post['id']}")
    assert delete_response.status_code == 204
