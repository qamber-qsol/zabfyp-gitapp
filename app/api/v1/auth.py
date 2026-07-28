import random
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_password_hash
from app.models.student import Student
from app.schemas.auth import EmailLookupRequest, OTPVerifyRequest
from app.services.email import send_otp_email

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/request-otp")
async def request_otp(request: EmailLookupRequest, db: Session = Depends(get_db)):
    clean_email = request.email.strip().lower()

    student = db.query(Student).filter(Student.email == clean_email).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found in the FYP 2026 registry. Contact your coordinator.",
        )

    otp_code = str(random.randint(100000, 999999))

    student.otp_code = otp_code
    student.otp_expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
    db.commit()

    try:
        await send_otp_email(email_to=clean_email, otp_code=otp_code)
    except Exception:
        student.otp_code = None
        student.otp_expires_at = None
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email. Please try again later.",
        )

    return {"message": "OTP sent successfully", "email": clean_email}


@router.post("/verify-otp")
async def verify_otp(request: OTPVerifyRequest, db: Session = Depends(get_db)):
    clean_email = request.email.strip().lower()
    student = db.query(Student).filter(Student.email == clean_email).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    if not student.otp_code or student.otp_code != request.otp_code:
        raise HTTPException(status_code=400, detail="Invalid OTP.")

    if student.otp_expires_at is None or student.otp_expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="OTP has expired.")

    student.hashed_password = get_password_hash(request.new_password)
    student.is_verified = True
    student.otp_code = None
    student.otp_expires_at = None

    db.commit()

    return {"message": "Account verified and password set successfully."}