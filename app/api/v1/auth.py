from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, generate_otp, get_password_hash, verify_password
from app.models.student import Student
from app.schemas.auth import LoginRequest, OTPRequest, OTPVerify, TokenResponse
from app.services.email import send_otp_email

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
) -> TokenResponse:
    clean_email = request.email.strip().lower()

    student = db.query(Student).filter(Student.email == clean_email).first()
    if not student or not student.hashed_password or not verify_password(request.password, student.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not student.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is not verified. Please verify your email first.",
        )

    access_token = create_access_token(data={"sub": student.email})
    return TokenResponse(access_token=access_token, token_type="bearer")


@router.post("/request-otp", status_code=status.HTTP_200_OK)
async def request_otp(
    request: OTPRequest,
    db: Session = Depends(get_db)
) -> dict[str, str]:
    clean_email = request.email.strip().lower()

    student = db.query(Student).filter(Student.email == clean_email).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student with this email address was not found.",
        )

    otp_code = generate_otp()
    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=15)

    student.otp_code = otp_code
    student.otp_expires_at = expiry_time

    db.commit()
    db.refresh(student)

    try:
        await send_otp_email(email_to=clean_email, otp_code=otp_code)
    except Exception as e:
        student.otp_code = None
        student.otp_expires_at = None
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send verification email: {str(e)}",
        )

    return {"message": "OTP sent successfully", "email": clean_email}


@router.post("/verify-otp", status_code=status.HTTP_200_OK)
async def verify_otp(
    request: OTPVerify,
    db: Session = Depends(get_db)
) -> dict[str, str]:
    clean_email = request.email.strip().lower()

    student = db.query(Student).filter(Student.email == clean_email).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student with this email address was not found.",
        )

    if not student.otp_code or student.otp_code != request.otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP code.",
        )

    expiry = student.otp_expires_at
    if expiry is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP code has expired or is invalid.",
        )

    now = datetime.now(timezone.utc)
    if expiry.tzinfo is None:
        expiry = expiry.replace(tzinfo=timezone.utc)

    if expiry < now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP code has expired.",
        )

    student.hashed_password = get_password_hash(request.new_password)
    student.is_verified = True
    student.otp_code = None
    student.otp_expires_at = None

    db.commit()
    db.refresh(student)

    return {"message": "Account verified and password set successfully."}