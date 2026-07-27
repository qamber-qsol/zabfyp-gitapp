from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    reg_id = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    group_id = Column(Integer, ForeignKey("project_groups.id"))
    invite_status = Column(String, default="pending")

    group = relationship("ProjectGroup", back_populates="students")