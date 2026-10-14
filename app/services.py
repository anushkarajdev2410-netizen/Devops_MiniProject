from .db import get_db

MAX_CREDITS_PER_SEMESTER = 18

def add_student(name, email):
    name, email = name.strip(), email.strip().lower()
    if not name or not email or "@" not in email:
        raise ValueError("A valid student name and email are required.")
    db = get_db()
    try:
        cur = db.execute("INSERT INTO students(name, email) VALUES (?, ?)", (name, email))
        db.commit()
        return cur.lastrowid
    except Exception as exc:
        db.rollback()
        if "UNIQUE constraint failed" in str(exc):
            raise ValueError("A student with this email already exists.") from exc
        raise

def add_faculty(name, department):
    if not name.strip() or not department.strip():
        raise ValueError("Faculty name and department are required.")
    db = get_db()
    cur = db.execute("INSERT INTO faculty(name, department) VALUES (?, ?)",
                     (name.strip(), department.strip()))
    db.commit()
    return cur.lastrowid

def add_course(code, title, credits):
    if not code.strip() or not title.strip():
        raise ValueError("Course code and title are required.")
    try:
        credits = int(credits)
    except (TypeError, ValueError) as exc:
        raise ValueError("Credits must be a positive integer.") from exc
    if credits <= 0:
        raise ValueError("Credits must be a positive integer.")
    db = get_db()
    try:
        cur = db.execute("INSERT INTO courses(code, title, credits) VALUES (?, ?, ?)",
                         (code.strip().upper(), title.strip(), credits))
        db.commit()
        return cur.lastrowid
    except Exception as exc:
        db.rollback()
        if "UNIQUE constraint failed" in str(exc):
            raise ValueError("A course with this code already exists.") from exc
        raise

def enroll_student(student_id, course_id, semester):
    if not semester or not semester.strip():
        raise ValueError("Semester is required.")
    db = get_db()
    student = db.execute("SELECT id FROM students WHERE id=?", (student_id,)).fetchone()
    course = db.execute("SELECT id, credits FROM courses WHERE id=?", (course_id,)).fetchone()
    if student is None:
        raise ValueError("Student not found.")
    if course is None:
        raise ValueError("Course not found.")
    existing = db.execute(
        "SELECT id FROM enrollments WHERE student_id=? AND course_id=? AND semester=?",
        (student_id, course_id, semester.strip())
    ).fetchone()
    if existing:
        raise ValueError("Student is already enrolled in this course for this semester.")
    total = db.execute(
        """SELECT COALESCE(SUM(c.credits), 0) AS total
           FROM enrollments e JOIN courses c ON c.id=e.course_id
           WHERE e.student_id=? AND e.semester=?""",
        (student_id, semester.strip())
    ).fetchone()["total"]
    if total + course["credits"] > MAX_CREDITS_PER_SEMESTER:
        raise ValueError("Enrollment exceeds the 18-credit semester limit.")
    cur = db.execute(
        "INSERT INTO enrollments(student_id, course_id, semester) VALUES (?, ?, ?)",
        (student_id, course_id, semester.strip())
    )
    db.commit()
    return cur.lastrowid

def record_marks(student_id, course_id, semester, score):
    try:
        score = float(score)
    except (TypeError, ValueError) as exc:
        raise ValueError("Score must be a number between 0 and 100.") from exc
    if not 0 <= score <= 100:
        raise ValueError("Score must be between 0 and 100.")
    db = get_db()
    enrolled = db.execute(
        "SELECT id FROM enrollments WHERE student_id=? AND course_id=? AND semester=?",
        (student_id, course_id, semester)
    ).fetchone()
    if not enrolled:
        raise ValueError("Student must be enrolled in the course before marks are recorded.")
    try:
        cur = db.execute(
            "INSERT INTO marks(student_id, course_id, semester, score) VALUES (?, ?, ?, ?)",
            (student_id, course_id, semester, score)
        )
        db.commit()
        return cur.lastrowid
    except Exception as exc:
        db.rollback()
        if "UNIQUE constraint failed" in str(exc):
            raise ValueError("Marks have already been recorded for this course and semester.") from exc
        raise

def grade_point(score):
    score = float(score)
    if score >= 90:
        return 10.0
    if score >= 80:
        return 9.0
    if score >= 70:
        return 8.0
    if score >= 60:
        return 7.0
    if score >= 50:
        return 6.0
    if score >= 40:
        return 5.0
    return 0.0

def calculate_gpa(student_id, semester):
    db = get_db()
    rows = db.execute(
        """SELECT m.score, c.credits
           FROM marks m JOIN courses c ON c.id=m.course_id
           WHERE m.student_id=? AND m.semester=?""",
        (student_id, semester)
    ).fetchall()
    if not rows:
        raise ValueError("No marks found for this student and semester.")
    total_credits = sum(row["credits"] for row in rows)
    weighted_points = sum(grade_point(row["score"]) * row["credits"] for row in rows)
    return round(weighted_points / total_credits, 2)

def list_students():
    return [dict(row) for row in get_db().execute("SELECT * FROM students ORDER BY id")]

def list_courses():
    return [dict(row) for row in get_db().execute("SELECT * FROM courses ORDER BY id")]

def list_faculty():
    return [dict(row) for row in get_db().execute("SELECT * FROM faculty ORDER BY id")]
