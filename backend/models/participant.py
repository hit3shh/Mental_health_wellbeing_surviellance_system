
import uuid
from datetime import datetime, timezone

from backend.extensions import db


class Participant(db.Model):
    __tablename__ = "participants"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    age_band = db.Column(db.String(20), nullable=True)

    consent_status = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    checkins = db.relationship(
        "CheckIn",
        back_populates="participant",
        cascade="all, delete-orphan"
    )
