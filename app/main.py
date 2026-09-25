from fastapi import FastAPI, HTTPException, Depends
from models import UserResponse, UserUpdate, BookResponse, BookUpdate, UserCreate, BookCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from database import User, Book
from sqlalchemy.orm import selectinload
import bcrypt 

app = FastAPI()

def hash_password(password: str):
  pwd_bytes = password.encode('utf-8')
  salt = bcrypt.gensalt()
  hashed = bcrypt.hashpw(pwd_bytes, salt)
  return hashed.decode('utf-8')


@app.get('/users', response_model=list[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)):        
  stmt = select(User)
  res = await db.execute(stmt)
  users = res.scalars().all()
  return users

@app.get('/users/{user_id}', response_model= UserResponse)
async def get_one_user(user_id: int,  db: AsyncSession = Depends(get_db)):
  stmt =  select(User).where(User.id == user_id)
  res = await db.execute(stmt)
  us = res.scalar_one_or_none()
  if not us:
    raise HTTPException(status_code=404, detail='user not found')
  return us

@app.get('/users/{user_id}/books', response_model=list[BookResponse])
async def get_books_of_one_user(user_id: int, db:AsyncSession = Depends(get_db)):
  stmt = select(Book).where(Book.user_id == user_id)
  res = await db.execute(stmt)
  books = res.scalars().all()
  if not books:
    raise HTTPException(status_code=404, detail='This user has no books')
  return books

@app.post('/users/create', response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate,  db: AsyncSession = Depends(get_db)):
  passw = hash_password(user.password)
  new_user = User(
    name = user.name, password= passw, email=user.email
  )
  db.add(new_user)
  await db.commit()
  await db.refresh(new_user)
  return new_user

@app.delete('/users/delete/{user_id}')
async def del_us(user_id: int,  db: AsyncSession = Depends(get_db)):
  stmt = select(User).options(selectinload(User.books)).where(User.id == user_id)
  res = await db.execute(stmt)
  us = res.scalar_one_or_none()
  if not us:
    raise HTTPException(status_code=404, detail='Can not find user with this id')
  else:
    await db.delete(us)
    await db.commit()
    return {"message": "User deleted"}



@app.put('/users/update/{user_id}', response_model=UserResponse)
async def up_us(user_id: int, us: UserUpdate,  db: AsyncSession = Depends(get_db)):
  stmt = select(User).where(User.id == user_id)
  res = await db.execute(stmt)
  up_user =  res.scalar_one_or_none()
  if not up_user:
    raise HTTPException(status_code=404, detail='User not found')
  if us.name is not None:
    up_user.name = us.name
  if us.email is not None:
    up_user.email = us.email                              
  if us.password is not None:
    hash_pas = hash_password(us.password)
    up_user.password = hash_pas
  await db.commit()
  return up_user




@app.get('/books', response_model=list[BookResponse])
async def get_all_books(db: AsyncSession = Depends(get_db)):
  stmt = select(Book)
  res = await db.execute(stmt)
  books = res.scalars().all()
  return books

@app.get('/books/{book_id}', response_model=BookResponse)
async def get_one_book(book_id: int,  db: AsyncSession = Depends(get_db)):
  stmt = select(Book).where(Book.id == book_id)
  res = await db.execute(stmt)
  book = res.scalar_one_or_none()
  if not book:
    raise HTTPException(status_code=404, detail='book not found')
  else:
    return book



@app.post('/books/create', response_model=BookResponse, status_code=201)
async def create_book(book: BookCreate,  db: AsyncSession = Depends(get_db)):
  new_book = Book(
    title = book.title, author = book.author, year=book.year, user_id = book.user_id
  )
  user = await db.get(User, book.user_id)
  if not user:
    raise HTTPException(status_code=404, detail='User not found')
  db.add(new_book)
  await db.commit()
  await db.refresh(new_book)
  return new_book

@app.delete('/books/delete/{book_id}')
async def del_book(book_id: int,  db: AsyncSession = Depends(get_db)):
  stmt = select(Book).where(Book.id == book_id)
  res = await db.execute(stmt)
  book = res.scalar_one_or_none()
  if not book:
    raise HTTPException(status_code=404, detail='Can not find user with this id')
  else:
    await db.delete(book)
    await db.commit()
    return {"message": "Book deleted"}



@app.put('/books/update/{book_id}', response_model=BookResponse)
async def up_book(book_id: int, book: BookUpdate,  db: AsyncSession = Depends(get_db)):
  stmt = select(Book).where(Book.id == book_id)
  res = await db.execute(stmt)
  up_book = res.scalar_one_or_none()
  if not up_book:
    raise HTTPException(status_code=404, detail='User not found')
  if book.title is not None:
    up_book.title = book.title
  if book.author is not None:
    up_book.author = book.author
  if book.year is not None:
    up_book.year = book.year
  await db.commit()
  return up_book
