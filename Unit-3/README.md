# Student Academic Management Platform

A beginner-friendly Flask API project for a DevOps assignment. It demonstrates student/faculty/course records, semester enrollments, an 18-credit semester cap, marks, GPA calculation, Pytest, Jenkins, Docker, and Minikube/Kubernetes.

## API
- `GET /api/health`
- `GET/POST /api/students`
- `GET/POST /api/faculty`
- `GET/POST /api/courses`
- `POST /api/enrollments`
- `POST /api/marks`
- `GET /api/students/<id>/gpa?semester=2026-Fall`

## Local development
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pytest -v
python run.py
```

## Docker
```bash
docker build -t student-academic-platform:v1.0.0 .
docker run --rm -p 5000:5000 student-academic-platform:v1.0.0
```

## Kubernetes
Build the image in the Minikube Docker environment, then apply:
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get pods -l app=student-academic-platform
kubectl get svc student-academic-service
```

Note: the sample Kubernetes manifest stores data in a temporary path per pod to keep the demo self-contained. It is not a shared persistent database configuration.
