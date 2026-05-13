from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from db.crud import *
from db.engine import create_db, sessionlocal
from jose import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')

create_db()

def get_db():
  db = sessionlocal()
  try:
    yield db
  finally:
    db.close()


def create_token(data: dict):
    '''Створюємо токен'''
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode = data.copy()
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    '''Перевіряємо токен'''
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username =  payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    '''Отримуємо поточного користувача'''
    payload = verify_token(token)
    username = payload.get("sub")
    user = get_user_db(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user






@app.post('/users')
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  new_user = create_user_db(db, user)
  return {'message': 'Successed', 'new_user': new_user}


@app.get('/books')
def get_books(author_id: int = Query(None, title='Author', description='Author`s name'), db: Session = Depends(get_db)):
  if author_id is None:
    return get_books_db(db)
  if author_id:
    return get_books_by_authors_db(db, author_id)


@app.post('/books')
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db),
                request_user: models.User = Depends(get_current_user)):
  new_book = create_book_db(db, book)
  return {'message': 'Successed', 'book': new_book}
  

@app.put('/books')
def update_book(book: schemas.BookCreate, db: Session = Depends(get_db),
                request_user: models.User = Depends(get_current_user)):
  upd_book = update_book_db(db, book.id, book)
  return {'message': 'Successed', 'book': upd_book}

@app.delete('/books')
def delete_book(book_id: int, db: Session = Depends(get_db),
                request_user: models.User = Depends(get_current_user)):
  deleted_book = delete_book_db(db, book_id)
  return {'message': 'Successed', 'book': deleted_book}

@app.post('/authors')
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db),
                  request_user: models.User = Depends(get_current_user)):
  new_author = create_author_db(db, author)
  return {'message': 'Successed', 'author': new_author}




















def get_current_user(
    token: str = Depends(oauth2_scheme),  # Отримуємо JWT токен через Depends
    db: Session = Depends(get_db),  # Отримуємо сесію бази даних
):
    """Отримуємо поточного користувача"""
    payload = verify_token(token)
    # Розшифровуємо та перевіряємо JWT токен.
    # verify_token() зазвичай:
    # - перевіряє підпис токена
    # - перевіряє expiration time
    # - повертає payload (dict)
    username = payload.get("sub") # Дістаємо username з поля "sub" (subject). У JWT "sub" часто використовується для ідентифікатора користувача.
    user = get_user_db(db, username) # Шукаємо користувача в базі даних за username.

    if not user:
        # Якщо користувача не знайдено — повертаємо помилку авторизації.
        raise HTTPException(status_code=401, detail="User not found")
    
    return user # Повертаємо об'єкт користувача.Тепер цей user можна використовувати в інших endpoints.




@app.post("/token") # Саме сюди клієнт надсилатиме логін і пароль для отримання JWT токена.
async def get_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    # Отримуємо дані форми:
    # - username
    # - password
    # FastAPI автоматично парсить form-data.
    db: Session = Depends(get_db),
    # Отримуємо сесію бази даних.
):
    """Отримуємо токен"""
    user_data = get_user_db(db, form_data.username) # Шукаємо користувача в БД по username.

    if not user_data:
        # Якщо користувача не знайдено —
        # повертаємо помилку авторизації.
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )

    if not pwd_context.verify(form_data.password, user_data.password):
        # Перевіряємо пароль.
        # form_data.password -> пароль який ввів користувач
        # user_data.password -> хешований пароль з БД
        # verify():
        # - хешує введений пароль
        # - порівнює з хешем у БД
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )
    access_token = create_token({"sub": user_data.username})
    # Створюємо JWT токен.
    # У payload кладемо:
    # "sub" -> username користувача.
    # Наприклад payload може виглядати так:
    # {
    #     "sub": "admin",
    #     "exp": 123456789
    # }
    # Повертаємо токен у форматі OAuth2.
    return {"access_token": access_token, "token_type": "bearer"}
