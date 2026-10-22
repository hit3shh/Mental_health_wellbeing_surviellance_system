
import pytest

from backend.app import create_app
from backend.extensions import db
from backend.models import Participant, CheckIn


@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite://",
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_checkin_page_loads(client):
    response = client.get("/checkin")
    assert response.status_code == 200
    assert b"How are you feeling today?" in response.data


def test_checkin_requires_demo_acknowledgement(client, app):
    response = client.post(
        "/checkin",
        data={
            "mood_rating": "4",
            "stress_rating": "2",
            "sleep_hours": "8",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"acknowledge" in response.data.lower()

    with app.app_context():
        assert CheckIn.query.count() == 0


def test_valid_checkin_is_saved(client, app):
    response = client.post(
        "/checkin",
        data={
            "mood_rating": "4",
            "stress_rating": "2",
            "sleep_hours": "8",
            "demo_ack": "yes",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Your demo check-in has been saved." in response.data

    with app.app_context():
        assert Participant.query.count() == 1
        assert CheckIn.query.count() == 1

        entry = CheckIn.query.first()
        assert entry.mood_rating == 4
        assert entry.stress_rating == 2
        assert entry.sleep_hours == 8.0


def test_invalid_rating_is_rejected(client, app):
    response = client.post(
        "/checkin",
        data={
            "mood_rating": "9",
            "stress_rating": "2",
            "sleep_hours": "8",
            "demo_ack": "yes",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Enter valid ratings" in response.data

    with app.app_context():
        assert CheckIn.query.count() == 0


def test_dashboard_shows_saved_checkin(client):
    client.post(
        "/checkin",
        data={
            "mood_rating": "4",
            "stress_rating": "2",
            "sleep_hours": "8",
            "demo_ack": "yes",
        },
    )

    response = client.get("/dashboard")

    assert response.status_code == 200
    assert b"4/5" in response.data
    assert b"2/5" in response.data
