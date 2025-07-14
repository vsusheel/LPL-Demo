from fastapi import FastAPI, Query, HTTPException, status
from typing import List, Optional
from .schemas import InventoryItem, UserAddBody
from uuid import uuid4
from datetime import datetime

app = FastAPI(title="Simple Inventory API", description="This is a simple API", version="1.0.0")

# In-memory storage for demonstration
inventory_db: List[InventoryItem] = []

# In-memory user storage
user_db = {}

@app.get("/inventory", response_model=List[InventoryItem], tags=["developers"])
def search_inventory(
    searchString: Optional[str] = Query(None, description="pass an optional search string for looking up inventory"),
    skip: int = Query(0, ge=0, description="number of records to skip for pagination"),
    limit: int = Query(10, ge=0, le=50, description="maximum number of records to return")
):
    results = inventory_db
    if searchString:
        results = [item for item in results if searchString.lower() in item.name.lower()]
    return results[skip:skip+limit]

@app.post("/inventory", response_model=InventoryItem, tags=["admins"], status_code=status.HTTP_201_CREATED)
def add_inventory(item: InventoryItem):
    # Check for duplicate by id
    for existing in inventory_db:
        if existing.id == item.id:
            raise HTTPException(status_code=409, detail="An existing item already exists")
    inventory_db.append(item)
    return item 

@app.post("/useradd", tags=["admins"], status_code=status.HTTP_201_CREATED)
def add_user(user: UserAddBody):
    if user.username in user_db:
        raise HTTPException(status_code=400, detail="User already exists")
    user_db[user.username] = user
    return {"message": "user created successfully"}

@app.delete("/useradd", tags=["admins"], status_code=status.HTTP_204_NO_CONTENT)
def delete_user(username: str = Query(..., description="username of the user to delete")):
    if username not in user_db:
        raise HTTPException(status_code=404, detail="user not found")
    del user_db[username]
    return None 