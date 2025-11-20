import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)

def test_signup_and_unregister():
    # Sign up a new participant
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert f"Signed up {email}" in signup_resp.json()["message"]

    # Unregister the participant
    unregister_resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unregister_resp.status_code == 200
    assert f"Unregistered {email}" in unregister_resp.json()["message"]

    # Unregister again should fail
    unregister_resp2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unregister_resp2.status_code == 400
    assert "not registered" in unregister_resp2.json()["detail"]

    # Sign up again should work
    signup_resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp2.status_code == 200
    assert f"Signed up {email}" in signup_resp2.json()["message"]

    # Duplicate signup should fail
    signup_resp3 = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp3.status_code == 400
    assert "already signed up" in signup_resp3.json()["detail"]

def test_signup_activity_not_found():
    resp = client.post("/activities/NonexistentActivity/signup?email=foo@bar.com")
    assert resp.status_code == 404
    assert "Activity not found" in resp.json()["detail"]

def test_unregister_activity_not_found():
    resp = client.post("/activities/NonexistentActivity/unregister?email=foo@bar.com")
    assert resp.status_code == 404
    assert "Activity not found" in resp.json()["detail"]
