# dependencies.py
from sqlalchemy.ext.asyncio import async_sessionmaker
from db import engine

session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

def get_session():
    return session