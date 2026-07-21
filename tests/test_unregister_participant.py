from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_student_from_activity():
    from src import app as app_module

    activity = app_module.activities["Chess Club"]
    original_participants = list(activity["participants"])
    email = "michael@mergington.edu"

    try:
        response = client.delete(f"/activities/Chess Club/participants/{email}")

        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from Chess Club"
        assert email not in activity["participants"]
    finally:
        activity["participants"] = original_participants


def test_unregister_participant_returns_404_for_unknown_student():
    response = client.delete("/activities/Chess Club/participants/unknown@example.com")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
