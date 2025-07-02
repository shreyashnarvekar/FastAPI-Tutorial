from pydantic import BaseModel, ConfigDict
from datetime import datetime


class NoteModel(BaseModel):
    id : str
    title : str
    content : str
    date_created : datetime
    
    model_config = ConfigDict(
        from_attributes = True
    )