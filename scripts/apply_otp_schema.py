from app.core.database import engine
from sqlalchemy import text

with engine.begin() as conn:
    conn.execute(text("ALTER TABLE students ADD COLUMN IF NOT EXISTS otp_code VARCHAR"))
    conn.execute(text("ALTER TABLE students ADD COLUMN IF NOT EXISTS otp_expires_at TIMESTAMP WITH TIME ZONE"))

print("schema updated")
