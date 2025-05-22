from pydantic import BaseModel

class Language:
    cpp = 'cpp'
    java = 'java'
    python = 'python'

class Code(BaseModel):
    language: Language
    filepath: str
