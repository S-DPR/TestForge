from dataclasses import dataclass

class Language:
    cpp = 'cpp'
    java = 'java'
    python = 'python'

@dataclass
class Code:
    language: Language
    filename: str
