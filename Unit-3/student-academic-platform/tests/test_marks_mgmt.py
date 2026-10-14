from app.services import add_student, add_course, enroll_student, record_marks, calculate_gpa, grade_point

def test_grade_point_bands():
    assert grade_point(95) == 10.0
    assert grade_point(85) == 9.0
    assert grade_point(75) == 8.0
    assert grade_point(35) == 0.0

def test_marks_and_weighted_gpa(app):
    with app.app_context():
        sid = add_student("Riya Shah", "riya@example.com")
        c1 = add_course("CS101", "Programming", 3)
        c2 = add_course("MA101", "Mathematics", 4)
        enroll_student(sid, c1, "2026-Fall")
        enroll_student(sid, c2, "2026-Fall")
        record_marks(sid, c1, "2026-Fall", 95)
        record_marks(sid, c2, "2026-Fall", 85)
        assert calculate_gpa(sid, "2026-Fall") == 9.43

def test_marks_require_enrollment(app):
    with app.app_context():
        sid = add_student("Riya Shah", "riya@example.com")
        cid = add_course("CS101", "Programming", 3)
        try:
            record_marks(sid, cid, "2026-Fall", 85)
            assert False, "Marks should require enrollment"
        except ValueError as exc:
            assert "must be enrolled" in str(exc)
