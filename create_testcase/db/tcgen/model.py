from datetime import datetime

from sqlalchemy.orm import relationship

from create_testcase.db.db import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, TIMESTAMP

class TcGen(Base):
    __tablename__ = "tcgen"

    tcgen_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), nullable=False)
    create_dt = Column(TIMESTAMP, nullable=False, default=datetime.now)

    blocks = relationship("TcGenBlock", back_populates="tcgen", cascade="all, delete-orphan")
    files = relationship("TcGenFile", back_populates="tcgen", cascade="all, delete-orphan")
