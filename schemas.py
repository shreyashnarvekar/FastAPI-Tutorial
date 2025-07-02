from pydantic import BaseModel, ConfigDict
from datetime import datetime
from pydantic import EmailStr
from typing import Optional


class NoteModel(BaseModel):
    id : str
    title : str
    content : str
    date_created : datetime
    
    model_config = ConfigDict(
        from_attributes = True
    )
    

class NoteCreateModel(BaseModel):
    title : str
    content : str
    
    model_config = ConfigDict(
        from_attributes = True,
        json_schema_extra={
            "example":{
                "title": "Sample title",
                "content":"Sample content"
            }
        }
    )
    
# USER MODEL

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    disabled: bool
    
    model_config = ConfigDict(from_attributes=True)

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None