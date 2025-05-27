from sqlalchemy import Column, TIMESTAMP, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from sqlalchemy.orm import relationship

from db.db import Base

class TcGenFile(Base):
    __tablename__ = "tcgen_file"

    tcgen_file_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tcgen_id = Column(UUID(as_uuid=True), ForeignKey("tcgen.tcgen_id", ondelete="CASCADE"), nullable=False)
    filepath = Column(Text, nullable=False)
    create_dt = Column(TIMESTAMP, nullable=False, default=datetime.now())

    tcgen = relationship("TcGen", back_populates="files")