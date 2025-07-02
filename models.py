from db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text
from datetime import datetime
from sqlalchemy import String
from typing import Optional

from sqlalchemy import String
from typing import Optional

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[Optional[str]] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
    disabled: Mapped[bool] = mapped_column(default=False)
    
    def __repr__(self):
        return f"<User {self.username}>"
    
 
class Note(Base):
    __tablename__ = 'notes'
    id : Mapped[str] = mapped_column(primary_key = True)
    title : Mapped[str] = mapped_column(nullable=False)
    content : Mapped[str] = mapped_column(Text, nullable=False)
    date_created : Mapped[datetime] = mapped_column(default=datetime.utcnow)
    owner_id: Mapped[int] = mapped_column(nullable=False)
    
    def __repr__(self) -> str:
        return f"<Note {self.title} at {self.date_created}"
