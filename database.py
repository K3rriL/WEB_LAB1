from pydantic import BaseModel
import mongoengine as me
from secret import DATABASE_URL

me.connect(host=DATABASE_URL)

class UserResponse(BaseModel):
    id: str
    email: str

class User(me.Document):
    email = me.StringField(required=True, unique=True)
    hashed_password = me.StringField(required=True)
    meta = {'collection': 'users'}
