from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []

items = [Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0)]

@app.post("/items/")
async def create_item(item: Item) -> Item:
    if item.name not in {items[i].name for i in range(len(items))}:
        items.append(item)
    return item


@app.get("/items/")
async def read_items() -> list[Item]:
    return items

