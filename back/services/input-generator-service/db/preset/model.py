from datetime import datetime

from db.db import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, TIMESTAMP, String

class Preset(Base):
    __tablename__ = "preset"

    preset_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    preset_name = Column(String(20), nullable=False)
    preset_type = Column(String, nullable=False)
    content = Column(String, nullable=False)
    account_id = Column(UUID(as_uuid=True), nullable=True)
    visibility = Column(String, nullable=False, default="PRIVATE")
    create_dt = Column(TIMESTAMP, nullable=False, default=datetime.now)
    update_dt = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
