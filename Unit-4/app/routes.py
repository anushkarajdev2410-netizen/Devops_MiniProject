from flask import Blueprint, jsonify, request
from . import services

api = Blueprint("api", __name__)

def error(message, status=400):
    return jsonify({"error": message}), status

@api.get("/health")
def health():
    return jsonify({"status": "healthy", "service": "student-academic-platform"}), 200

@api.get("/")
def index():
    return jsonify({
        "application": "Student Academic Management Platform",
        "endpoints": [
            "GET /api/health", "GET/POST /api/students", "GET/POST /api/faculty",
            "GET/POST /api/courses", "POST /api/enrollments", "POST /api/marks",
            "GET /api/students/<id>/gpa?semester=..."
        ]
    })

@api.get("/students")
def get_students():
    return jsonify(services.list_students())

@api.post("/students")
def create_student():
    data = request.get_json(silent=True) or {}
    try:
        student_id = services.add_student(data.get("name", ""), data.get("email", ""))
        return jsonify({"id": student_id, "message": "Student created"}), 201
    except ValueError as exc:
        return error(str(exc))

@api.get("/faculty")
def get_faculty():
    return jsonify(services.list_faculty())

@api.post("/faculty")
def create_faculty():
    data = request.get_json(silent=True) or {}
    try:
        faculty_id = services.add_faculty(data.get("name", ""), data.get("department", ""))
        return jsonify({"id": faculty_id, "message": "Faculty created"}), 201
    except ValueError as exc:
        return error(str(exc))

@api.get("/courses")
def get_courses():
    return jsonify(services.list_courses())

@api.post("/courses")
def create_course():
    data = request.get_json(silent=True) or {}
    try:
        course_id = services.add_course(data.get("code", ""), data.get("title", ""), data.get("credits"))
        return jsonify({"id": course_id, "message": "Course created"}), 201
    except ValueError as exc:
        return error(str(exc))

@api.post("/enrollments")
def create_enrollment():
    data = request.get_json(silent=True) or {}
    try:
        enrollment_id = services.enroll_student(
            int(data.get("student_id", 0)), int(data.get("course_id", 0)), data.get("semester", "")
        )
        return jsonify({"id": enrollment_id, "message": "Enrollment created"}), 201
    except (ValueError, TypeError) as exc:
        return error(str(exc))

@api.post("/marks")
def create_marks():
    data = request.get_json(silent=True) or {}
    try:
        marks_id = services.record_marks(
            int(data.get("student_id", 0)), int(data.get("course_id", 0)),
            data.get("semester", ""), data.get("score")
        )
        return jsonify({"id": marks_id, "message": "Marks recorded"}), 201
    except (ValueError, TypeError) as exc:
        return error(str(exc))

@api.get("/students/<int:student_id>/gpa")
def get_gpa(student_id):
    semester = request.args.get("semester", "")
    try:
        return jsonify({"student_id": student_id, "semester": semester,
                        "gpa": services.calculate_gpa(student_id, semester)}), 200
    except ValueError as exc:
        return error(str(exc), 404)
