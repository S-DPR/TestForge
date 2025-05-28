from datetime import datetime
from sqlalchemy import Column, TIMESTAMP, Text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from db.db import Base

class CodeRes(Base):
    __tablename__ = "code_res"

    code_res_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tcgen_file_id = Column(UUID(as_uuid=True), ForeignKey("code_file.code_file_id"), nullable=False)
    input_filepath = Column(Text, nullable=False)
    exitcode = Column(Integer, nullable=False)
    # execute_time = Column(Integer, nullable=False)  # ms
    # memory = Column(Integer, nullable=False)  # KB
    output_filepath = Column(Text, nullable=False)
    create_dt = Column(TIMESTAMP, nullable=False, default=datetime.now)

    file = relationship("CodeFile", backref="results", cascade="all, delete-orphan")