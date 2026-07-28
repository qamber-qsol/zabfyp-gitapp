import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.group import ProjectGroup
from app.models.student import Student

db = SessionLocal()

# 1. Create a dummy group
test_group = ProjectGroup(
    group_name="Mock FYP Test",
    repo_name="fyp2026-p9-99-mocktest",
    team_name="team-fyp2026-p9-99-mocktest",
    status="pending"
)
db.add(test_group)
db.commit()
db.refresh(test_group)

# 2. Attach your email to this group
test_student = Student(
    name="Coordinator Test",
    email="mscs2573122@szabist.pk",
    group_id=test_group.id
)
db.add(test_student)
db.commit()

print(f"✅ Mock group '{test_group.repo_name}' injected with email {test_student.email}")
db.close()