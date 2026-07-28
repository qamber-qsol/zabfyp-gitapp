from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class SystemComment(Base):
    __tablename__ = "system_comments"

    id = Column(Integer, primary_key=True, index=True)
    push_event_id = Column(Integer, ForeignKey("push_events.id"), nullable=True)
    group_id = Column(Integer, ForeignKey("project_groups.id"), nullable=True)
    author_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    push_event = relationship("PushEvent", back_populates="comments")
    group = relationship("ProjectGroup", back_populates="comments")
    author = relationship("Student", back_populates="comments")

