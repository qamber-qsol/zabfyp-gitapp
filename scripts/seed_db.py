import os
import sys
import re
import pandas as pd

# Add root directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.group import ProjectGroup
from app.models.student import Student

def slugify(text: str) -> str:
    # Preserves original casing but replaces spaces/special characters with hyphens
    text = str(text).strip()
    return re.sub(r'[\W_]+', '-', text)

def seed():
    db = SessionLocal()
    csv_path = os.path.join("data", "all-fyp-groups.csv")
    
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        return

    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} groups from CSV. Seeding NeonDB...")

    for _, row in df.iterrows():
        group_no = str(row['group-no']).strip()
        group_name = str(row['group-name']).strip()
        
        repo_name = f"fyp2026-{group_no}-{slugify(group_name)}"
        team_name = f"team-{repo_name}"

        # 1. Create or query ProjectGroup
        group = db.query(ProjectGroup).filter_by(group_no=group_no).first()
        if not group:
            group = ProjectGroup(
                group_no=group_no,
                group_name=group_name,
                repo_name=repo_name,
                team_name=team_name
            )
            db.add(group)
            db.commit()
            db.refresh(group)

        # 2. Add Members (up to 3)
        for i in range(1, 4):
            reg_col = f'member-{i} id'
            email_col = f'member-{i} email'
            name_col = f'member-{i} name'

            if pd.notna(row[reg_col]) and pd.notna(row[email_col]):
                reg_id = str(row[reg_col]).split('.')[0].strip()
                email = str(row[email_col]).strip()
                name = str(row[name_col]).strip()

                existing_student = db.query(Student).filter_by(reg_id=reg_id).first()
                if not existing_student:
                    student = Student(
                        reg_id=reg_id,
                        name=name,
                        email=email,
                        group_id=group.id
                    )
                    db.add(student)

    db.commit()
    db.close()
    print("✅ Database seeding complete!")

if __name__ == "__main__":
    seed()