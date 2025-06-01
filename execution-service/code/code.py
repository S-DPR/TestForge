from pydantic import BaseModel
from enum import Enum

class Language(str, Enum):
    cpp = 'cpp'
    java = 'java'
    python = 'python'

class Code(BaseModel):
    language: Language
    filepath: str
