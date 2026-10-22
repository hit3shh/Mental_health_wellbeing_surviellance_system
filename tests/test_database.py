
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


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_database_connection(client):
    response = client.get("/health/database")
    assert response.status_code == 200
    assert response.json["database"] == "connected"


def test_participant_and_checkin_creation(app):
    with app.app_context():
        participant = Participant(
            age_band="13-15",
            consent_status=True,
        )
        db.session.add(participant)
        db.session.flush()

        checkin = CheckIn(
            participant_id=participant.id,
            mood_rating=4,
            stress_rating=2,
            sleep_hours=8.0,
        )
        db.session.add(checkin)
        db.session.commit()

        saved = db.session.get(CheckIn, checkin.id)
        assert saved is not None
        assert saved.participant_id == participant.id
        assert saved.mood_rating == 4
