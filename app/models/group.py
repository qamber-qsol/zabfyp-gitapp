from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class ProjectGroup(Base):
    __tablename__ = "project_groups"

    id = Column(Integer, primary_key=True, index=True)
    group_no = Column(String, unique=True, index=True)
    group_name = Column(String)
    repo_name = Column(String, unique=True)
    team_name = Column(String, unique=True)
    status = Column(String, default="pending")
    github_repo_url = Column(String, nullable=True)

    students = relationship("Student", back_populates="group")