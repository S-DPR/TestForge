from datetime import datetime
from sqlalchemy import Column, TIMESTAMP, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from db.db import Base

class CodeFile(Base):
    __tablename__ = "code_file"

    code_file_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), nullable=False)
    language = Column(Text, nullable=False)
    filepath = Column(Text, nullable=False)
    extension = Column(Text, nullable=False)

    result = relationship("CodeRes", backref="result", cascade="all, delete-orphan")
