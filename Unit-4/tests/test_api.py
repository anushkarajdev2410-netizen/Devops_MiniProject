def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"

def test_create_student_endpoint(client):
    response = client.post("/api/students", json={
        "name": "Asha Patil", "email": "asha@example.com"
    })
    assert response.status_code == 201
    assert response.get_json()["id"] == 1

def test_invalid_student_is_rejected(client):
    response = client.post("/api/students", json={"name": "", "email": "bad"})
    assert response.status_code == 400
