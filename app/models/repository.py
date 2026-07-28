from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class GroupRepository(Base):
    __tablename__ = "group_repositories"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("project_groups.id"), unique=True, nullable=False)
    repo_name = Column(String, nullable=False)
    status = Column(String, default="pending_creation")

    group = relationship("ProjectGroup", backref="repository")


class StudentGithubInvite(Base):
    __tablename__ = "student_github_invites"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    github_username = Column(String, nullable=False)
    invite_status = Column(String, default="pending")

    student = relationship("Student", backref="github_invite")
