from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class BaseS(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class UserMod(BaseS):
  name: str
  password: str
  email: EmailStr
  id: int

class UserResponse(BaseS):
  name: str
  email: str
  id: int


class UserUpdate(BaseS):
  name: Optional[str] = None
  email: Optional[EmailStr] = None
  password: Optional[str] = None

class UserCreate(BaseS):
  name: str
  email: EmailStr
  password: str

class BookMod(BaseS):
  title: str
  author: str
  year: int
  user_id: int
  id: int

class BookResponse(BaseS):
  title: str
  author: str
  year: int
  user_id: int
  id: int

class BookUpdate(BaseS):
  title: Optional[str] = None
  author: Optional[str] = None
  year: Optional[int] = None

class BookCreate(BaseS):
  title: str
  author: str
  year: int
  user_id: int


