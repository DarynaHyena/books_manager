from pydantic import BaseModel, Field
from datetime import date
from datetime import datetime, timezone

class AuthorBase(BaseModel):
  first_name: str
  last_name: str
  bio: str
  birthdate: date

class AuthorCreate(AuthorBase):
  pass

class AuthorUpdate(AuthorBase):
  pass

class Author(AuthorBase):
  id: int
  created_at: date











class BookBase(BaseModel):
  title: str
  description: str
  pages: int
  year: int
  image: str = None
  author_id: int

class BookCreate(BookBase):
  pass

class BookUpdate(BookBase):
  pass

class Book(BookBase):
  id: int
  author_id: int
  author: Author
  created_at: date




class UserBase(BaseModel):
  username: str
  password: str

class UserCreate(UserBase):
  email: str

class UserLogin(BaseModel):
  pass
class User(UserBase):
  id: int
  email: str
  created_at: datetime
