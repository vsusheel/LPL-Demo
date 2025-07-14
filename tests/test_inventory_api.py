from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4
from datetime import datetime
from app.schemas import UserAddBody

client = TestClient(app)

def make_item(id=None, name="Widget Adapter"):
    return {
        "id": str(id or uuid4()),
        "name": name,
        "releaseDate": datetime.utcnow().isoformat() + "Z",
        "manufacturer": {
            "name": "ACME Corporation",
            "homePage": "https://www.acme-corp.com",
            "phone": "408-867-5309"
        }
    }

def test_get_inventory_empty():
    response = client.get("/inventory")
    assert response.status_code == 200
    assert response.json() == []

def test_post_inventory():
    item = make_item()
    response = client.post("/inventory", json=item)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == item["name"]
    assert data["id"] == item["id"]
    assert data["manufacturer"]["name"] == item["manufacturer"]["name"]

def test_post_inventory_duplicate():
    item = make_item()
    client.post("/inventory", json=item)
    response = client.post("/inventory", json=item)
    assert response.status_code == 409

def test_get_inventory_after_post():
    item = make_item()
    client.post("/inventory", json=item)
    response = client.get("/inventory")
    assert response.status_code == 200
    data = response.json()
    assert any(x["id"] == item["id"] for x in data)

def test_search_inventory():
    item = make_item(name="Widget Adapter")
    client.post("/inventory", json=item)
    response = client.get("/inventory?searchString=Widget")
    assert response.status_code == 200
    data = response.json()
    assert any("Widget" in x["name"] for x in data)

def test_pagination():
    # Add more items
    for i in range(2, 7):
        item = make_item(name=f"Item{i}")
        client.post("/inventory", json=item)
    response = client.get("/inventory?skip=2&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2 

def test_add_user():
    user = {"username": "alice", "password": "secret", "email": "alice@example.com"}
    response = client.post("/useradd", json=user)
    assert response.status_code == 201
    assert response.json()["message"] == "user created successfully"

def test_add_duplicate_user():
    user = {"username": "bob", "password": "secret", "email": "bob@example.com"}
    client.post("/useradd", json=user)
    response = client.post("/useradd", json=user)
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"

def test_delete_user():
    user = {"username": "charlie", "password": "secret", "email": "charlie@example.com"}
    client.post("/useradd", json=user)
    response = client.delete("/useradd", params={"username": "charlie"})
    assert response.status_code == 204

def test_delete_nonexistent_user():
    response = client.delete("/useradd", params={"username": "ghost"})
    assert response.status_code == 404
    assert response.json()["detail"] == "user not found" 