from fastapi import APIRouter

router = APIRouter()


@router.get("/me")
def get_current_student():
    return {"message": "Student self-service scaffold"}
