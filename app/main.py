from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
from .schemas import InventoryItem

app = FastAPI(title="Simple Inventory API", description="This is a simple API", version="1.0.0")

# In-memory storage for demonstration
inventory_db: List[InventoryItem] = []

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

@app.post("/inventory", response_model=InventoryItem, tags=["admins"])
def add_inventory(item: InventoryItem):
    item.id = len(inventory_db) + 1
    inventory_db.append(item)
    return item 