from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, Mapped, DeclarativeBase, mapped_column, relationship
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL=os.getenv('DATABASE_URL')

engine = create_async_engine(DATABASE_URL, echo = False)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_db():
  async with AsyncSessionLocal() as db:
          yield db



class Base(DeclarativeBase):
  pass

class User(Base):
  __tablename__ = 'users'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str]
  email: Mapped[str]
  password: Mapped[str]
  books =  relationship('Book', back_populates='user', cascade='all, delete-orphan', lazy='selectin') #По умолчанию используется lazy='select', что подразумевает ленивую загрузку при обращении к атрибуту. В асинхронной сессии (AsyncSession) ленивая загрузка вызывает неявный ввод-вывод, который не поддерживается и приводит к ошибке MissingGreenlet (или sqlalchemy.exc.MissingGreenlet). Решение: укажите lazy='selectin' или lazy='joined' для relationship, либо всегда используйте явные запросы с опциями selectinload() / joinedload().

class Book(Base):
  __tablename__ = 'books'
  id: Mapped[int] = mapped_column(primary_key=True)
  title: Mapped[str]
  author: Mapped[str]
  year: Mapped[int]
  user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
  user = relationship('User', back_populates='books', lazy='selectin')

async def create_tables():
  async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
  asyncio.run(create_tables())
