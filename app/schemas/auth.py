from pydantic import BaseModel, EmailStr, Field


class OTPRequest(BaseModel):
    email: EmailStr


class OTPVerify(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6, description="6-digit OTP code")
    new_password: str = Field(..., min_length=8, description="New password with minimum length of 8")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# Aliases for backward compatibility
EmailLookupRequest = OTPRequest
OTPVerifyRequest = OTPVerify


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

