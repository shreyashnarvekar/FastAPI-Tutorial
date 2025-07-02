from models import Note, User
from sqlalchemy import select
from schemas import UserCreate
from passlib.context import CryptContext
from dependencies import get_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CRUD:
    def get_password_hash(self, password: str):
        return pwd_context.hash(password)

    async def get_user_by_username(self, username: str):
        session = get_session()
        async with session() as session:
            statement = select(User).filter(User.username == username)
            result = await session.execute(statement)
            return result.scalars().first()

    async def create_user(self, user: UserCreate):
        hashed_password = self.get_password_hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        session = get_session()
        async with session() as session:
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
        return db_user

    async def get_all_notes(self, user_id: int):
        session = get_session()
        async with session() as session:
            statement = select(Note).filter(Note.owner_id == user_id).order_by(Note.id)
            result = await session.execute(statement)
            return result.scalars()

    async def add_note(self, note: Note):
        session = get_session()
        async with session() as session:
            session.add(note)
            await session.commit()
        return note

    async def get_note_by_id(self, note_id: str):
        session = get_session()
        async with session() as session:
            statement = select(Note).filter(Note.id == note_id)
            result = await session.execute(statement)
            return result.scalars().one()

    async def update_note(self, note_id: str, data: dict):
        session = get_session()
        async with session() as session:
            statement = select(Note).filter(Note.id == note_id)
            result = await session.execute(statement)
            note = result.scalars().one()
            
            note.title = data['title']
            note.content = data['content']
            
            await session.commit()
            return note

    async def delete_note(self, note: Note):
        session = get_session()
        async with session() as session:
            await session.delete(note)
            await session.commit()
        return {}