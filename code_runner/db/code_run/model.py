from datetime import datetime
from sqlalchemy import Column, TIMESTAMP, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from create_testcase.db.db import Base

class CodeRun(Base):
    __tablename__ = "code_run"

    code_run_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), nullable=False)
    language = Column(Text, nullable=False)
    create_dt = Column(TIMESTAMP, nullable=False, default=datetime.now)

    file = relationship("CodeFile", backref="results", cascade="all, delete-orphan")
