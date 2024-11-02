from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
messages = {}

class Message(BaseModel):
    id: int | None = 0
    author: str
    content: str
    tags: list[str] = []

@app.post("/messages/", response_model=Message)
async def create_message(message: Message) -> Message:
    new_id = max(messages.keys(), default=0) + 1
    if new_id in messages:
        raise HTTPException(status_code=400, detail="Message with this id alredy exists")
    new_message = Message(id=new_id, author=message.author, content=message.content, tags=message.tags)
    messages[new_id] = new_message
    return messages[new_id]

@app.get("/messages/")
async def read_items() -> messages:
    return messages

