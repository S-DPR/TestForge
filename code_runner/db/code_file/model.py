from datetime import datetime
from sqlalchemy import Column, TIMESTAMP, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from db.db import Base

class CodeFile(Base):
    __tablename__ = "code_file"

    code_file_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code_run_id = Column(UUID(as_uuid=True), ForeignKey("code_run.code_run_id"), nullable=False)
    filepath = Column(Text, nullable=False)
    extension = Column(Text, nullable=False)

    run = relationship("CodeRun", backref="files", cascade="all, delete-orphan")
    result = relationship("CodeRes", backref="result", cascade="all, delete-orphan")
