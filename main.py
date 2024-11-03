from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import User, UserResponse

app = FastAPI()
messages = {}

class Message(BaseModel):
    id: int | None = 0
    author: str
    content: str
    tags: list[str] = []

# Users rules
@app.post("/users/", response_model=UserResponse)
async def create_user(email: str, password: str):
    if User.objects(email=email).first():
        raise HTTPException(status_code=400, detail="User with this email already registered")
    user = User(email=email, hashed_password=password)
    user.save()
    return UserResponse(id=str(user.id), email=user.email)

@app.get("/users/{email}", response_model=UserResponse)
async def get_user(email:str):
    user = User.objects(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with this email not found")
    return UserResponse(id=str(user.id), email=user.email)

# Messages
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

