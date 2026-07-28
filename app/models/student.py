import enum

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class UserRole(str, enum.Enum):
    STUDENT = "student"
    COORDINATOR = "coordinator"
    ADMIN = "admin"


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    reg_id = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    group_id = Column(Integer, ForeignKey("project_groups.id"))
    invite_status = Column(String, default="pending")
    hashed_password = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.STUDENT, nullable=False)
    is_verified = Column(Boolean, default=False)
    github_username = Column(String, unique=True, nullable=True)
    otp_code = Column(String, nullable=True)
    otp_expires_at = Column(DateTime(timezone=True), nullable=True)

    @property
    def otp_expiry(self):
        return self.otp_expires_at

    @otp_expiry.setter
    def otp_expiry(self, value):
        self.otp_expires_at = value

    group = relationship("ProjectGroup", back_populates="students")
    comments = relationship("SystemComment", back_populates="author")