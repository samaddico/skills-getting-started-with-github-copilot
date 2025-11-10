from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app


def test_get_activities():
    client = TestClient(app)
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # basic sanity: one of the seeded activities exists
    assert "Chess Club" in data


def test_signup_and_unregister():
    client = TestClient(app)
    activity = "Chess Club"
    email = "test.user@example.com"

    # Ensure the test email is not already registered
    resp = client.get("/activities")
    assert resp.status_code == 200
    assert email not in resp.json()[activity]["participants"]

    # Sign up
    signup_path = f"/activities/{quote(activity)}/signup?email={quote(email)}"
    resp = client.post(signup_path)
    assert resp.status_code == 200
    assert "Signed up" in resp.json()["message"]

    # Confirm participant is listed
    resp = client.get("/activities")
    assert email in resp.json()[activity]["participants"]

    # Unregister the participant
    delete_path = f"/activities/{quote(activity)}/participants?email={quote(email)}"
    resp = client.delete(delete_path)
    assert resp.status_code == 200
    assert "Unregistered" in resp.json()["message"]

    # Confirm participant removed
    resp = client.get("/activities")
    assert email not in resp.json()[activity]["participants"]
