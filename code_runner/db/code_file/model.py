from datetime import datetime
from sqlalchemy import Column, TIMESTAMP, Text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from db.db import Base

class CodeFile(Base):
    __tablename__ = "code_file"
    __table_args__ = (
        Index("ix_codefile_code_account_lang", "code", "account_id", "language"),
    )

    code_file_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), nullable=False)
    language = Column(Text, nullable=False)
    filepath = Column(Text, nullable=False, unique=True, index=True)
    code = Column(Text, nullable=False, unique=True)

    result = relationship("CodeRes", back_populates="result", cascade="all, delete-orphan")
