import random
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db # Assuming you created this dependency
from app.models.student import Student
from app.schemas.auth import EmailLookupRequest
from app.services.email import send_otp_email

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/request-otp")
async def request_otp(request: EmailLookupRequest, db: Session = Depends(get_db)):
    # 1. Sanitize the input
    clean_email = request.email.strip().lower()
    
    # 2. Database Lookup
    student = db.query(Student).filter(Student.email == clean_email).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found in the FYP 2026 registry. Contact your coordinator."
        )
    
    # 3. Generate a secure 6-digit OTP
    otp_code = str(random.randint(100000, 999999))
    
    # TODO: In the next step, we will save this OTP to the database/Redis with an expiration timestamp.
    
    # 4. Dispatch Email
    try:
        await send_otp_email(email_to=clean_email, otp_code=otp_code)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email. Please try again later."
        )
    
    return {"message": "OTP sent successfully", "email": clean_email}