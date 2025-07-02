from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker
from crud import CRUD
from db import engine

app = FastAPI(
    title = "Noted API",
    description = "This is simple note taking service",
    docs_url = "/"
)

session = async_sessionmaker(
    bind = engine,
    expire_on_commit= False
)

db = CRUD()


@app.get('/notes')
async  def get_all_notes():
    notes = await db.get_all(session)
    return notes

@app.post('/notes')
async  def create_note():
    pass

@app.get('/note/{note_id}')
async  def get_note_by_id(note_id):
    pass

@app.patch('/note/{note_id}')
async  def update_note(note_id):
    pass

@app.delete('/note/{note_id}')
async  def delete_note(note_id):
    pass