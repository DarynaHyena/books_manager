from fastapi import HTTPException
from . import schemas, models
from sqlalchemy.orm import Session
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def get_books_db(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Book).offser(skip).limit(limit).all()

def create_book_db(db: Session, book: schemas.BookCreate):
  author = db.query(models.Author).filter(models.Author.id == book.author_id).first()
  if not author:
    raise HTTPException(status_code=404)
  
  new_book = models.Book(title=book.title, description=book.description, pages=book.pages, year=book.year, image=book.image, author_id=book.author_id)
  db.add(new_book)
  db.commit()
  db.refresh(new_book)

  return new_book

def update_book_db(db: Session, book_id: int, book: schemas.BookUpdate):
  upd_book = db.query(models.Book).filter(models.Book.id == book_id).first()
  if not upd_book:
    raise HTTPException(status_code=404)
  if not upd_book:
    raise HTTPException(status_code=404)
  
  upd_book.title = book.title
  upd_book.description = book.description
  upd_book.pages = book.pages
  upd_book.year = book.year
  upd_book.image = book.image
  upd_book.author_id = book.author_id

  db.commit()
  db.refresh(upd_book)

  return upd_book

def delete_book_db(db: Session, book_id: int):
  book = db.query(models.Book).filter(models.Book.id == book_id).first()
  if not book:
    raise HTTPException(status_code=404)
  
  db.delete(book)
  db.commit()
  db.refresh(book)

  return book


def get_books_by_authors_db(db: Session, author_id: int):
  books = db.query(models.Book).filter(models.Book.author_id).all()
  if not books:
    raise HTTPException(status_code=404)
  
  return books

def create_author_db(db: Session, author: schemas.AuthorCreate):
  new_author = models.Author(
    first_name=author.first_name,
    last_name=author.last_name,
    bio=author.bio,
    birthdate=author.birthdate
    )
  
  db.add(new_author)
  db.commit()
  db.refresh(new_author)

  return new_author





def get_user_db(db: Session, username: str):
  return db.query(models.User).filter(models.User.username == username).first()

def create_user_db(db: Session, user: schemas.UserCreate):
  if db.query(models.User).filter(models.User.username == user.username).first():
    raise HTTPException(status_code=404)
    
  if db.query(models.User).filter(models.User.email == user.email).first():
    raise HTTPException(status_code=404)
    
  new_user = models.User(username=user.username,email=user.username, password=pwd_context.hash(user.password))
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

