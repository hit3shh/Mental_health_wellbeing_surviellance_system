
from datetime import datetime, timezone

from backend.extensions import db


class CheckIn(db.Model):
    __tablename__ = "checkins"

    id = db.Column(db.Integer, primary_key=True)

    participant_id = db.Column(
        db.String(36),
        db.ForeignKey("participants.id"),
        nullable=False,
        index=True,
    )

    mood_rating = db.Column(db.Integer, nullable=False)
    stress_rating = db.Column(db.Integer, nullable=False)
    sleep_hours = db.Column(db.Float, nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    participant = db.relationship(
        "Participant",
        back_populates="checkins",
    )

    __table_args__ = (
        db.CheckConstraint(
            "mood_rating BETWEEN 1 AND 5",
            name="check_mood_rating",
        ),
        db.CheckConstraint(
            "stress_rating BETWEEN 1 AND 5",
            name="check_stress_rating",
        ),
        db.CheckConstraint(
            "sleep_hours IS NULL OR "
            "(sleep_hours >= 0 AND sleep_hours <= 24)",
            name="check_sleep_hours",
        ),
    )
