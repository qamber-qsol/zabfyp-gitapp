from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class PushEvent(Base):
    __tablename__ = "push_events"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("project_groups.id"))
    commit_hash = Column(String, unique=True)
    timestamp = Column(String)
    approval_status = Column(String, default="pending")

    comments = relationship("SystemComment", back_populates="push_event")