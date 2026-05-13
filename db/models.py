from .engine import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy.sql import func

class Book(Base):
  __tablename__ = 'books'

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String(30), unique=True)
  description = Column(String(150), unique=True)
  pages = Column(Integer)
  year = Column(Integer)
  image = Column(String(200), nullable=True)
  created_at = Column(DateTime, default=datetime.now(timezone.utc))

  author_id = Column(Integer, ForeignKey('authors.id'))
  author = relationship("Author", back_populates='books')



class Author(Base):
  __tablename__ = 'authors'

  id = Column(Integer, primary_key=True, index=True)
  first_name = Column(String(30))
  last_name = Column(String(30))
  bio = Column(String(150))
  birthdate = Column(Integer)
  created_at = Column(DateTime(timezone=True), server_default=func.now())

  books = relationship("Book", back_populates='author')



class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, nullable=False)
  email = Column(String, unique=True, nullable=True)
  password = Column(String, nullable=False)

  created_at = Column(DateTime(timezone=True), server_default=func.now())
