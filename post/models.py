from db.base import Base

class PostBase(BaseModel):
    title: str
    content: str
