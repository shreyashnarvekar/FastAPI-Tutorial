from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models import Note
import uuid
from schemas import NoteModel, NoteCreateModel, UserCreate, Token, User
from auth import (
    get_current_active_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user
)
from auth import create_tokens, refresh_access_token
from datetime import timedelta
from crud import CRUD

app = FastAPI(
    title="Noted API",
    description="This is simple note taking service",
    docs_url="/"
)

db = CRUD()

# Authentication routes
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token, refresh_token = create_tokens(data={"sub": user.username})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
    
@app.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    return await refresh_access_token(refresh_token)

@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    db_user = await db.get_user_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await db.create_user(user)

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# Note routes
@app.get('/notes', response_model=list[NoteModel])
async def get_all_notes(current_user: User = Depends(get_current_active_user)):
    notes = await db.get_all_notes(current_user.id)
    return notes

@app.post('/notes', status_code=status.HTTP_201_CREATED)
async def create_note(
    note_data: NoteCreateModel,
    current_user: User = Depends(get_current_active_user)
):
    new_note = Note(
        id=str(uuid.uuid4()),
        title=note_data.title,
        content=note_data.content,
        owner_id=current_user.id
    )
    note = await db.add_note(new_note)
    return note

@app.get('/note/{note_id}', response_model=NoteModel)
async def get_note_by_id(
    note_id: str,
    current_user: User = Depends(get_current_active_user)
):
    note = await db.get_note_by_id(note_id)
    if note.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this note"
        )
    return note

@app.patch('/note/{note_id}', response_model=NoteModel)
async def update_note(
    note_id: str,
    data: NoteCreateModel,
    current_user: User = Depends(get_current_active_user)
):
    note = await db.get_note_by_id(note_id)
    if note.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this note"
        )
    
    updated_note = await db.update_note(note_id, {
        'title': data.title,
        'content': data.content
    })
    return updated_note

@app.delete('/note/{note_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: str,
    current_user: User = Depends(get_current_active_user)
):
    note = await db.get_note_by_id(note_id)
    if note.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this note"
        )
    await db.delete_note(note)
    return None