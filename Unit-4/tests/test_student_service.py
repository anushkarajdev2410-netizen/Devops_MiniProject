from app.services import add_student, add_course, enroll_student
from app.db import get_db

def test_student_can_be_created(app):
    with app.app_context():
        student_id = add_student("Asha Patil", "asha@example.com")
        row = get_db().execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
        assert row["name"] == "Asha Patil"

def test_duplicate_student_email_is_rejected(app):
    with app.app_context():
        add_student("Asha Patil", "asha@example.com")
        try:
            add_student("Another Name", "asha@example.com")
            assert False, "Duplicate email should be rejected"
        except ValueError as exc:
            assert "already exists" in str(exc)

def test_enrollment_cannot_exceed_18_credits(app):
    with app.app_context():
        sid = add_student("Asha Patil", "asha@example.com")
        c1 = add_course("CS101", "Computer Science", 10)
        c2 = add_course("MA101", "Mathematics", 9)
        enroll_student(sid, c1, "2026-Fall")
        try:
            enroll_student(sid, c2, "2026-Fall")
            assert False, "Credit limit should be enforced"
        except ValueError as exc:
            assert "18-credit" in str(exc)

def test_same_course_cannot_be_enrolled_twice(app):
    with app.app_context():
        sid = add_student("Asha Patil", "asha@example.com")
        cid = add_course("CS101", "Computer Science", 3)
        enroll_student(sid, cid, "2026-Fall")
        try:
            enroll_student(sid, cid, "2026-Fall")
            assert False, "Duplicate enrollment should be rejected"
        except ValueError as exc:
            assert "already enrolled" in str(exc)
