from datetime import datetime

from sqlalchemy.orm import relationship

from db.db import Base
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from sqlalchemy import Column, TIMESTAMP, Integer, Text, ForeignKey


class TcGenBlock(Base):
    __tablename__ = "tcgen_block"

    tcgen_block_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tcgen_id = Column(UUID(as_uuid=True), ForeignKey("tcgen.tcgen_id", ondelete="CASCADE"), nullable=False)

    type = Column(Text, nullable=False)
    config = Column(JSONB, nullable=True)
    variable = Column(JSONB, nullable=True)
    output = Column(JSONB, nullable=True)
    repeat = Column(Text, nullable=True)
    sequence = Column(Integer, nullable=False)

    create_dt = Column(TIMESTAMP, nullable=True, default=datetime.now)

    tcgen = relationship("TcGen", back_populates="blocks")
