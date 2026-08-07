import random
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from fastapi_mail import FastMail, MessageSchema, MessageType

from app.core.database import get_db
from app.models.group import ProjectGroup
from app.models.student import Student
from app.services.email import send_otp_email, conf
from app.services.github_client import github_service

router = APIRouter()

class GroupResponse(BaseModel):
    id: int
    group_no: str | None
    group_name: str | None

class MemberResponse(BaseModel):
    id: int
    name: str | None
    email: str
    reg_id: str | None

class RequestOTP(BaseModel):
    email: EmailStr

class VerifyOTP(BaseModel):
    email: EmailStr
    otp: str

class GithubInvite(BaseModel):
    email: EmailStr
    github_username: str

class ChangeEmailRequest(BaseModel):
    old_email: EmailStr
    new_email: EmailStr
    student_name: str
    student_id: int
    group_id: int
    group_name: str

@router.get("/groups", response_model=list[GroupResponse])
def get_groups(db: Session = Depends(get_db)):
    return db.query(ProjectGroup).all()

@router.get("/groups/{group_id}/members", response_model=list[MemberResponse])
def get_group_members(group_id: int, db: Session = Depends(get_db)):
    group = db.query(ProjectGroup).filter(ProjectGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group.students

@router.post("/request-otp")
async def request_otp(data: RequestOTP, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.email == data.email).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    otp = f"{random.randint(100000, 999999)}"
    student.otp_code = otp
    student.otp_expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
    db.commit()
    
    await send_otp_email(student.email, otp)
    return {"message": "OTP sent successfully"}

@router.post("/verify-otp")
def verify_otp(data: VerifyOTP, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.email == data.email).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if student.otp_code != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    if student.otp_expires_at and student.otp_expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="OTP expired")
    
    student.otp_code = None
    db.commit()
    db.refresh(student)
    
    group = student.group
    return {
        "student": {
            "id": student.id,
            "name": student.name,
            "email": student.email,
        },
        "group": {
            "id": group.id if group else None,
            "group_name": group.group_name if group else None,
            "group_no": group.group_no if group else None,
            "github_repo_url": group.github_repo_url if group else None
        }
    }

@router.post("/github-invite")
def github_invite(data: GithubInvite, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.email == data.email).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.github_username = data.github_username
    db.commit()
    
    group = student.group
    if not group:
        raise HTTPException(status_code=400, detail="Student has no group")
    
    if not group.repo_name or not group.team_name:
        raise HTTPException(status_code=400, detail="Group repository or team not set up")
    
    results = github_service.provision_group(
        repo_name=group.repo_name,
        team_name=group.team_name,
        student_emails=[student.email]
    )
    
    if results.get("errors"):
        raise HTTPException(status_code=400, detail=f"GitHub invite failed: {results['errors']}")
        
    return {"message": "Invite dispatched successfully"}

@router.post("/change-email-request")
async def change_email_request(data: ChangeEmailRequest):
    html_content = f"""
    <h3>Email Change Request</h3>
    <p>Student Name: {data.student_name} (ID: {data.student_id})</p>
    <p>Group: {data.group_name} (ID: {data.group_id})</p>
    <p>Old Email: {data.old_email}</p>
    <p>New Email: {data.new_email}</p>
    """
    
    message = MessageSchema(
        subject="Student Email Change Request",
        recipients=["qambar.ali@szabist.pk"],
        body=html_content,
        subtype=MessageType.html,
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message": "Support request sent successfully"}
